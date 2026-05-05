import sys
import os

import streamlit as st

from utils.styles import inject_styles, page_header, section_title

st.set_page_config(
    page_title="Model Insights – OnchoAI",
    page_icon="🧠",
    layout="wide",
)
inject_styles()

page_header(
    "🧠",
    "Model Insights & Architecture",
    "Understand how OnchoAI processes tissue images and infers drug recommendations."
)

# ── System Overview ───────────────────────────────────────────────────────────
section_title("System Overview")

st.markdown("""
<div class="card">
  <p style="color:#94A3B8; line-height:1.9; margin:0; font-size:0.95rem;">
    This framework follows a <strong style="color:#00C9A7;">Subtype-Guided Drug Recommendation Strategy</strong>.
    The system does <em>not</em> directly predict drug response from images. Instead, it builds an
    intermediate tumour phenotype representation that links histopathology to pharmacogenomics.
  </p>
</div>
""", unsafe_allow_html=True)

# Pipeline flow
pipeline = [
    ("1", "Image Input",            "Histopathology tissue slide uploaded by user."),
    ("2", "CNN Feature Extraction", "ResNet-18 extracts 512-dim morphological embeddings."),
    ("3", "Graph Construction",     "Nuclei detected and modelled as a spatial cellular graph."),
    ("4", "GCN Encoding",           "Graph Convolutional Network encodes structural behaviour."),
    ("5", "Feature Fusion",         "CNN + GNN embeddings concatenated into unified vector."),
    ("6", "Subtype Inference",      "KMeans clustering assigns tumour to phenotype subtype."),
    ("7", "Drug Ranking",           "GDSC IC50 data used to rank drugs per subtype."),
]

st.markdown("<br>", unsafe_allow_html=True)
for step in pipeline:
    num, title, desc = step
    st.markdown(f"""
    <div style="display:flex; align-items:flex-start; gap:14px; margin-bottom:0.75rem;">
      <div style="min-width:32px; height:32px; border-radius:50%;
                  background:rgba(0,201,167,0.15); border:1.5px solid rgba(0,201,167,0.4);
                  display:flex; align-items:center; justify-content:center;
                  font-weight:700; color:#00C9A7; font-size:0.85rem; flex-shrink:0;">
        {num}
      </div>
      <div style="padding-top:4px;">
        <span style="font-weight:600; color:#E2E8F0;">{title}</span>
        <span style="color:#64748B;"> — {desc}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ── EVALUATION METRICS ──────────────────────────────
import numpy as np
import plotly.graph_objects as go

section_title("Model Evaluation Metrics")

st.markdown("""
<p style="color:#64748B; font-size:0.9rem; margin-bottom:1.5rem;">
  "Performance metrics for each component of the OnchoAI pipeline.").
</p>
""", unsafe_allow_html=True)

st.markdown("""
<div style="font-weight:600; color:#E2E8F0; font-size:1rem; margin-bottom:0.75rem;">
  🧠 CNN Open-Set Validator — ResNet-18
</div>
""", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
for col, (label, val, color) in zip([m1, m2, m3, m4], [
    ("Final Accuracy",  "99.62%", "#00C9A7"),
    ("Final Loss",      "2.27",   "#EF4444"),
    ("Training Epochs", "10",     "#3B82F6"),
    ("Dataset Size",    "11,031", "#F59E0B"),
]):
    with col:
        st.markdown(f"""
        <div style="background:#111827; border:1px solid #1E293B; border-top:3px solid {color};
                    border-radius:10px; padding:1rem; text-align:center;">
          <div style="font-size:1.6rem; font-weight:700; color:{color};">{val}</div>
          <div style="color:#64748B; font-size:0.8rem; margin-top:4px;">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Training curves — values from phase3a_cnn_feature_extraction.ipynb logs
epochs       = list(range(1, 11))
accuracy_log = [93.30, 97.22, 98.19, 98.57, 98.68, 98.87, 99.35, 99.30, 99.41, 99.62]
loss_log     = [27.40, 11.52,  7.89,  6.23,  6.98,  5.12,  3.26,  3.04,  2.47,  2.27]

col_a, col_l = st.columns(2)

with col_a:
    fig_a = go.Figure()
    fig_a.add_trace(go.Scatter(
        x=epochs, y=accuracy_log, mode="lines+markers",
        line=dict(color="#00C9A7", width=2.5), marker=dict(size=7),
        fill="tozeroy", fillcolor="rgba(0,201,167,0.07)",
    ))
    fig_a.update_layout(
        title="Training Accuracy (%) per Epoch",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E2E8F0",
        xaxis=dict(title="Epoch", gridcolor="#1E293B", tickvals=epochs),
        yaxis=dict(title="Accuracy (%)", gridcolor="#1E293B", range=[90, 101]),
        title_font_size=13, height=280, margin=dict(t=40, b=40), showlegend=False,
    )
    st.plotly_chart(fig_a, use_container_width=True)

with col_l:
    fig_l = go.Figure()
    fig_l.add_trace(go.Scatter(
        x=epochs, y=loss_log, mode="lines+markers",
        line=dict(color="#EF4444", width=2.5), marker=dict(size=7),
        fill="tozeroy", fillcolor="rgba(239,68,68,0.07)",
    ))
    fig_l.update_layout(
        title="Training Loss per Epoch",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E2E8F0",
        xaxis=dict(title="Epoch", gridcolor="#1E293B", tickvals=epochs),
        yaxis=dict(title="Loss", gridcolor="#1E293B"),
        title_font_size=13, height=280, margin=dict(t=40, b=40), showlegend=False,
    )
    st.plotly_chart(fig_l, use_container_width=True)


st.markdown("""
<div style="font-weight:600; color:#E2E8F0; font-size:1rem; margin-bottom:0.75rem;">
  🔲 KMeans Pseudo-Confusion Matrix
</div>
""", unsafe_allow_html=True)

import plotly.express as px


labels_cm = ["Benign (0)", "Malignant (1)"]
cm = np.array([
    [1162, 1318],
    [1400, 4029],
])
fig_cm = px.imshow(
    cm, labels=dict(x="Predicted (Cluster)", y="Actual (BreaKHis Label)", color="Count"),
    x=labels_cm, y=labels_cm, text_auto=True,
    color_continuous_scale=[[0, "#0A0E1A"], [0.5, "#1E3A5F"], [1, "#00C9A7"]],
    aspect="auto", title="Pseudo-Confusion Matrix — KMeans Cluster vs BreaKHis Ground-Truth",
)
fig_cm.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font_color="#E2E8F0", title_font_size=13, height=320,
    coloraxis_colorbar=dict(bgcolor="rgba(0,0,0,0)", tickfont=dict(color="#E2E8F0")),
)
st.plotly_chart(fig_cm, use_container_width=True)
st.caption("⚠️ This is an unsupervised pseudo-confusion matrix — KMeans cluster assignments mapped to binary BreaKHis labels. Not a supervised classifier evaluation.")


st.markdown("""
<div style="font-weight:600; color:#E2E8F0; font-size:1rem; margin:1.5rem 0 0.75rem;">
  🔗 Cellular GNN (Graph Convolutional Network)
</div>
""", unsafe_allow_html=True)

g1, g2, g3 = st.columns(3)
for col, (label, val, color, desc) in zip([g1, g2, g3], [
    ("Training Images",         "7,909",  "#00C9A7", "BreaKHis histology slides (2,480 benign / 5,429 malignant)"),
    ("Training Epochs",         "20",     "#3B82F6",  "Best loss: 141.45 (Epoch 1) → 253.76 (Epoch 20)"),
    ("GNN Embedding Dimension", "64",     "#8B5CF6",  "Output feature vector size per graph"),
]):
    with col:
        st.markdown(f"""
        <div style="background:#111827; border:1px solid #1E293B; border-top:3px solid {color};
                    border-radius:10px; padding:1rem; text-align:center;">
          <div style="font-size:1.5rem; font-weight:700; color:{color};">{val}</div>
          <div style="color:#64748B; font-size:0.78rem; margin-top:4px;">{label}</div>
          <div style="color:#334155; font-size:0.7rem; margin-top:4px;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style="font-weight:600; color:#E2E8F0; font-size:1rem; margin:1rem 0 0.75rem;">
  🔬 Phenotype Clustering — KMeans (k=3)
</div>
""", unsafe_allow_html=True)

km1, km2, km3, km4 = st.columns(4)
for col, (label, val, color) in zip([km1, km2, km3, km4], [
    ("Silhouette Score",  "0.455", "#00C9A7"),
    ("PCA Components",    "2",     "#3B82F6"),
    ("Input Feature Dim", "576",   "#8B5CF6"),
    ("Num. Subtypes",     "3",     "#F59E0B"),
]):
    with col:
        st.markdown(f"""
        <div style="background:#111827; border:1px solid #1E293B; border-top:3px solid {color};
                    border-radius:10px; padding:1rem; text-align:center;">
          <div style="font-size:1.5rem; font-weight:700; color:{color};">{val}</div>
          <div style="color:#64748B; font-size:0.8rem; margin-top:4px;">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style="font-weight:600; color:#E2E8F0; font-size:1rem; margin:1rem 0 0.75rem;">
  📊 KMeans Subtype Distribution &amp; Pseudo-Accuracy (vs BreaKHis ground-truth)
</div>
""", unsafe_allow_html=True)

col_dist, col_pa = st.columns(2)

with col_dist:
    subtype_counts = {"Indolent-like": 3912, "Moderate-like": 1435, "Aggressive-like": 2562}
    fig_dist = px.bar(
        x=list(subtype_counts.keys()),
        y=list(subtype_counts.values()),
        color=list(subtype_counts.keys()),
        color_discrete_map={
            "Indolent-like":   "#00C9A7",
            "Moderate-like":   "#F59E0B",
            "Aggressive-like": "#EF4444",
        },
        title="Cluster Assignment Distribution (n=7,909)",
        labels={"x": "Subtype", "y": "Image Count"},
    )
    fig_dist.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E2E8F0", showlegend=False,
        title_font_size=13, height=260, margin=dict(t=40, b=40),
        xaxis=dict(gridcolor="#1E293B"), yaxis=dict(gridcolor="#1E293B"),
    )
    st.plotly_chart(fig_dist, use_container_width=True)

with col_pa:
    st.markdown("""
    <div style="background:#111827; border:1px solid #1E293B; border-radius:10px; padding:1.1rem;">
      <div style="color:#94A3B8; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.4px; margin-bottom:0.75rem;">
        Pseudo-Accuracy vs BreaKHis Labels
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.6rem;">
        <div style="text-align:center; background:#0A0E1A; border-radius:8px; padding:0.6rem;">
          <div style="font-size:1.3rem; font-weight:700; color:#00C9A7;">70%</div>
          <div style="color:#64748B; font-size:0.72rem; margin-top:2px;">Pseudo Accuracy</div>
        </div>
        <div style="text-align:center; background:#0A0E1A; border-radius:8px; padding:0.6rem;">
          <div style="font-size:1.3rem; font-weight:700; color:#3B82F6;">74.8%</div>
          <div style="color:#64748B; font-size:0.72rem; margin-top:2px;">F1 Score</div>
        </div>
        <div style="text-align:center; background:#0A0E1A; border-radius:8px; padding:0.6rem;">
          <div style="font-size:1.3rem; font-weight:700; color:#8B5CF6;">75.4%</div>
          <div style="color:#64748B; font-size:0.72rem; margin-top:2px;">Precision</div>
        </div>
        <div style="text-align:center; background:#0A0E1A; border-radius:8px; padding:0.6rem;">
          <div style="font-size:1.3rem; font-weight:700; color:#F59E0B;">74.2%</div>
          <div style="color:#64748B; font-size:0.72rem; margin-top:2px;">Recall</div>
        </div>
      </div>
      <div style="color:#475569; font-size:0.72rem; margin-top:0.75rem; line-height:1.5;">
        ⚠️ Unsupervised clustering — these scores measure alignment with binary
        ground-truth labels, not direct supervised classification accuracy.
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
# ── END OF EVALUATION METRICS BLOCK ──────────────────────────────────────────



# ── Image Side ────────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)

with c1:
    section_title("Image-Side Intelligence")
    img_items = [
        ("🖼️", "CNN – ResNet-18",       "Extracts 512-dim morphological feature vectors from tissue slides."),
        ("🔗", "Graph Construction",    "Nuclei detected via Otsu thresholding, centroids used as graph nodes."),
        ("📡", "GCN",                   "Graph Convolutional Network encodes spatial nuclear interactions."),
        ("🔀", "Feature Fusion",        "CNN + GNN embeddings fused into a 576-dim unified tumour vector."),
    ]
    for icon, title, desc in img_items:
        st.markdown(f"""
        <div style="display:flex; gap:10px; margin-bottom:0.75rem; padding:0.75rem;
                    background:#111827; border:1px solid #1E293B; border-radius:10px;">
          <span style="font-size:1.2rem; flex-shrink:0;">{icon}</span>
          <div>
            <div style="font-weight:600; color:#E2E8F0; font-size:0.88rem;">{title}</div>
            <div style="color:#64748B; font-size:0.8rem; margin-top:2px; line-height:1.5;">{desc}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

with c2:
    section_title("Subtype Inference Layer")
    subtypes = [
        ("🟢", "Indolent-like",    "#00C9A7", "Low aggressiveness. Cells appear well-organised with low nuclear irregularity."),
        ("🟡", "Moderate-like",   "#F59E0B", "Intermediate phenotype. Mixed morphological signals."),
        ("🔴", "Aggressive-like", "#EF4444", "High aggressiveness. Dense, irregular nuclei with rapid division markers."),
    ]
    for emoji, name, color, desc in subtypes:
        st.markdown(f"""
        <div style="border-left:3px solid {color}; padding:0.75rem 1rem; margin-bottom:0.75rem;
                    background:#111827; border-radius:0 10px 10px 0;">
          <div style="font-weight:600; color:{color}; font-size:0.9rem;">{emoji} {name}</div>
          <div style="color:#64748B; font-size:0.8rem; margin-top:4px; line-height:1.5;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

with c3:
    section_title("Drug Recommendation Strategy")
    st.markdown("""
    <div class="card">
      <div style="color:#64748B; font-size:0.85rem; line-height:1.8;">
        Drug recommendations are <strong style="color:#E2E8F0;">not synthetic</strong>.<br><br>
        They are grounded in real pharmacogenomic data:
        <ul style="margin:0.75rem 0 0; padding-left:1.2rem; color:#94A3B8;">
          <li>GDSC pharmacogenomic dataset</li>
          <li>Subtype-level IC50 aggregation</li>
          <li>Drug sensitivity ranking per subtype</li>
        </ul>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Design Guarantees ─────────────────────────────────────────────────────────
section_title("Design Guarantees")

guarantees = [
    ("✅", "No Synthetic Supervision",        "All labels and scores derived from real biological data."),
    ("✅", "No Direct IC50 Prediction",       "System never predicts IC50 from images — avoids confounding."),
    ("✅", "Pharmacogenomic Grounding",        "Recommendations backed by GDSC sensitivity trends."),
    ("✅", "Research-Consistent Design",       "Architecture follows established computational pathology norms."),
    ("✅", "Explainability Built-In",          "Grad-CAM + SHAP provide visual and statistical interpretability."),
]

g1, g2 = st.columns(2)
for i, (icon, title, desc) in enumerate(guarantees):
    with (g1 if i % 2 == 0 else g2):
        st.markdown(f"""
        <div style="display:flex; gap:10px; margin-bottom:0.6rem; padding:0.8rem 1rem;
                    background:#111827; border:1px solid #1E293B; border-radius:10px;">
          <span style="color:#00C9A7; font-size:1rem; flex-shrink:0;">{icon}</span>
          <div>
            <div style="font-weight:600; color:#E2E8F0; font-size:0.88rem;">{title}</div>
            <div style="color:#64748B; font-size:0.8rem; margin-top:2px;">{desc}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
