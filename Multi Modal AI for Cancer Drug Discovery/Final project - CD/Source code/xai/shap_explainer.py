import shap
import numpy as np
import joblib
import os

BASE_PATH = r"E:\Final_Year_Project"

SCALER_PATH = os.path.join(BASE_PATH, "models", "scaler.pkl")
KMEANS_PATH = os.path.join(BASE_PATH, "models", "kmeans_model.pkl")
PCA_PATH = os.path.join(BASE_PATH, "models", "pca_model.pkl")


def compute_shap_values(feature_vector):

    scaler = joblib.load(SCALER_PATH)
    kmeans = joblib.load(KMEANS_PATH)
    pca = joblib.load(PCA_PATH)

    # Background (use small random subset or same input)
    background = feature_vector

    def model_fn(x):
        x_scaled = scaler.transform(x)
        x_reduced = pca.transform(x_scaled)