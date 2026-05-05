import os
import cv2
import numpy as np
import torch
import joblib
import pandas as pd
import torch.nn as nn
import torch.nn.functional as F

from torch_geometric.data import Data
from torch_geometric.nn import GCNConv, global_mean_pool
from torchvision.models import resnet18, ResNet18_Weights
from torchvision import transforms


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

SCALER_PATH = os.path.join(BASE_PATH, "models", "scaler.pkl")
KMEANS_PATH = os.path.join(BASE_PATH, "models", "kmeans_model.pkl")
PCA_PATH = os.path.join(BASE_PATH, "models", "pca_model.pkl")
GNN_MODEL_PATH = os.path.join(BASE_PATH, "models", "cellular_gnn_trained.pt")
CNN_VALIDATOR_PATH = os.path.join(BASE_PATH, "models", "cnn_open_set_validator.pt")
SUBTYPE_MAP_PATH = os.path.join(BASE_PATH, "models", "subtype_mapping.pkl")

RANKING_PATH = os.path.join(
    BASE_PATH,
    "outputs",
    "drug_ranking",
    "subtype_specific_drug_ranking.csv"
)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# --------------------------------------------------
# CELLULAR GNN
# --------------------------------------------------

class CellularGNN(torch.nn.Module):

    def __init__(self, in_channels):
        super().__init__()

        self.conv1 = GCNConv(in_channels, 32)
        self.conv2 = GCNConv(32, 64)
        self.classifier = nn.Linear(64, 2)

    def forward(self, x, edge_index, batch):

        x = self.conv1(x, edge_index)
        x = F.relu(x)

        x = self.conv2(x, edge_index)
        x = F.relu(x)

        x = global_mean_pool(x, batch)

        logits = self.classifier(x)

        return logits, x


# --------------------------------------------------
# LOAD MODELS
# --------------------------------------------------

def load_models():

    scaler = joblib.load(SCALER_PATH)
    kmeans = joblib.load(KMEANS_PATH)
    pca = joblib.load(PCA_PATH)
    subtype_mapping = joblib.load(SUBTYPE_MAP_PATH)

    # ---------------- Validator CNN ----------------
    validator_model = resnet18(weights=ResNet18_Weights.DEFAULT)
    validator_model.fc = nn.Linear(validator_model.fc.in_features, 3)

    validator_model.load_state_dict(
        torch.load(CNN_VALIDATOR_PATH, map_location=DEVICE)
    )

    validator_model = validator_model.to(DEVICE)
    validator_model.eval()

    # ---------------- Feature CNN ----------------
    feature_cnn = resnet18(weights=ResNet18_Weights.DEFAULT)
    feature_cnn.fc = nn.Identity()

    feature_cnn = feature_cnn.to(DEVICE)
    feature_cnn.eval()

    # ---------------- GNN ----------------
    gnn_model = CellularGNN(in_channels=5).to(DEVICE)

    gnn_model.load_state_dict(
        torch.load(GNN_MODEL_PATH, map_location=DEVICE)
    )

    gnn_model.eval()

    return validator_model, feature_cnn, gnn_model, scaler, kmeans, pca, subtype_mapping

# --------------------------------------------------
# LOAD MODELS ONCE (GLOBAL)
# --------------------------------------------------

validator_model, feature_cnn, gnn_model, scaler, kmeans, pca, subtype_mapping = load_models()

# --------------------------------------------------
# IMAGE TRANSFORM
# --------------------------------------------------

transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


# --------------------------------------------------
# IMAGE VALIDATION
# --------------------------------------------------

def validate_image(image_path):

    img = cv2.imread(image_path)

    if img is None:
        return False, 0.0

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_tensor = transform(img).unsqueeze(0).to(DEVICE)

    with torch.no_grad():

        logits = validator_model(img_tensor)
        probs = F.softmax(logits, dim=1)

    predicted_class = torch.argmax(probs, dim=1).item()
    confidence = torch.max(probs).item()

    if predicted_class == 2:
        return False, confidence

    if confidence < 0.60:
        return False, confidence

    return True, confidence


# --------------------------------------------------
# CNN FEATURE EXTRACTION
# --------------------------------------------------

def extract_cnn_features(image_path):

    img = cv2.imread(image_path)

    if img is None:
        return np.zeros(512, dtype=np.float32)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_tensor = transform(img).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        features = feature_cnn(img_tensor)

    features = features.cpu().numpy().astype(np.float32).squeeze()

    # Safety check
    features = np.nan_to_num(features)

    return features


# --------------------------------------------------
# GNN FEATURE EXTRACTION
# --------------------------------------------------

def extract_gnn_features(image_path):

    img = cv2.imread(image_path)

    if img is None:
        return np.zeros(64, dtype=np.float32)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh = cv2.threshold(
        blur,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    kernel = np.ones((3, 3), np.uint8)

    open_img = cv2.morphologyEx(
        thresh,
        cv2.MORPH_OPEN,
        kernel,
        iterations=2
    )

    close_img = cv2.morphologyEx(
        open_img,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=2
    )

    contours, _ = cv2.findContours(
        close_img,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    centroids = []
    node_features = []

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area <= 0:
            continue

        perimeter = cv2.arcLength(cnt, True)

        circularity = (
            4 * np.pi * area / (perimeter ** 2)
            if perimeter > 0 else 0
        )

        M = cv2.moments(cnt)

        if M["m00"] != 0:

            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            centroids.append((cx, cy))

            x, y, w, h = cv2.boundingRect(cnt)

            aspect_ratio = float(w) / h if h > 0 else 0
            rect_area = w * h
            extent = float(area) / rect_area if rect_area > 0 else 0

            node_features.append([
                area,
                perimeter,
                circularity,
                aspect_ratio,
                extent
            ])

    if len(node_features) < 2:
        return np.zeros(64, dtype=np.float32)

    node_features = np.array(node_features, dtype=np.float32)

    # NORMALIZATION
    node_features = (node_features - node_features.mean(axis=0)) / (node_features.std(axis=0) + 1e-8)

    node_features = torch.tensor(node_features, dtype=torch.float).to(DEVICE)

    edge_index = []

    for i, c1 in enumerate(centroids):
        for j, c2 in enumerate(centroids):

            if i != j:

                dist = np.linalg.norm(
                    np.array(c1) - np.array(c2)
                )

                if dist <= 30:
                    edge_index.append([i, j])

    if len(edge_index) == 0:
        return np.zeros(64, dtype=np.float32)

    edge_index = torch.tensor(
        edge_index,
        dtype=torch.long
    ).t().contiguous().to(DEVICE)

    data = Data(x=node_features, edge_index=edge_index)

    batch = torch.zeros(
        data.x.size(0),
        dtype=torch.long
    ).to(DEVICE)

    with torch.no_grad():

        _, embedding = gnn_model(
            data.x,
            data.edge_index,
            batch
        )

    embedding = embedding.cpu().numpy().astype(np.float32).squeeze()

    embedding = np.nan_to_num(embedding)

    return embedding


# --------------------------------------------------
# SUBTYPE PREDICTION
# --------------------------------------------------

def predict_subtype(fused_features):

    fused_features = fused_features.astype(np.float32)

    scaled = scaler.transform(fused_features)

    reduced = pca.transform(scaled) 

    cluster_label = kmeans.predict(reduced)[0]

    return subtype_mapping[cluster_label]


# --------------------------------------------------
# DRUG RECOMMENDATION
# --------------------------------------------------

def recommend_drugs(subtype):

    ranking_df = pd.read_csv(RANKING_PATH)

    subtype_df = ranking_df[ranking_df["Subtype"] == subtype]

    if subtype_df.empty:
        return None

    result = subtype_df[["Drug Name", "IC50", "Compatibility Score"]].copy()

    result.columns = ["Drug", "IC50", "Score"]

    result = result.sort_values(by="Score", ascending=False)

    return result.head(20)

# --------------------------------------------------
# MASTER INFERENCE FUNCTION
# --------------------------------------------------

def run_inference(image_path):

    is_valid, confidence = validate_image(image_path)

    if not is_valid:
        return f"Rejected: Not a histopathology image (Confidence: {confidence:.2f})", None, None
    
    cnn_feat = extract_cnn_features(image_path)

    gnn_feat = extract_gnn_features(image_path)

    fused_features = np.hstack(
        [cnn_feat, gnn_feat]
    ).reshape(1, -1).astype(np.float32)

    fused_features = np.nan_to_num(fused_features)

    subtype = predict_subtype(fused_features)

    drugs = recommend_drugs(subtype)

    return subtype, drugs, fused_features