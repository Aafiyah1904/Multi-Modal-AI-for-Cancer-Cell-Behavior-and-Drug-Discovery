import sys
import os

import streamlit as st

from utils.styles import inject_styles, page_header, section_title

st.set_page_config(
    page_title="About – OnchoAI",
    page_icon="📘",
    layout="wide",
)
inject_styles()

page_header(
    "📘",
    "About This Project",
    "Phenotype-driven, subtype-guided drug recommendation using computational pathology."
)

# ── Problem Statement ─────────────────────────────────────────────────────────
section_title("Problem Statement")

st.markdown("""
<div class="card">
  <p style="color:#94A3B8; line-height:1.8; margin:0;">
    Traditional drug recommendation systems often rely purely on genomic data.
    However, tumour morphology contains rich <strong style="color:#E2E8F0;">phenotypic signals</strong>
    that are rarely leveraged for therapeutic guidance.<br><br>
    This project proposes a <strong style="color:#00C9A7;">phenotype-driven, subtype-guided</strong>
    drug recommendation framework that integrates computational pathology and
    pharmacogenomic intelligence — with no synthetic supervision.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Datasets ──────────────────────────────────────────────────────────────────
section_title("Datasets Used")

d1, d2, d3 = st.columns(3)

datasets = [
    ("🔬", "BreaKHis Dataset",
     "Histopathology images for tumour morphology modelling across 4 magnification levels.",
     "#00C9A7"),
    ("🧪", "ChEMBL Database",
     "Molecular structures and IC50 bioactivity records used for drug feature extraction.",
     "#3B82F6"),
    ("📊", "GDSC Dataset",
     "Genomics of Drug Sensitivity in Cancer — subtype-level drug sensitivity trends.",
     "#8B5CF6"),
]

for col, (icon, name, desc, color) in zip([d1, d2, d3], datasets):
    with col:
        st.markdown(f"""
        <div class="card" style="border-top: 3px solid {color};">
          <div style="font-size:1.8rem; margin-bottom:0.6rem;">{icon}</div>
          <div style="font-weight:600; color:#E2E8F0; margin-bottom:0.4rem;">{name}</div>
          <div style="color:#64748B; font-size:0.85rem; line-height:1.6;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Technologies ──────────────────────────────────────────────────────────────
section_title("Technologies Used")

techs = [
    ("🐍", "Python 3.10"),
    ("🔦", "PyTorch"),
    ("📡", "PyTorch Geometric"),
    ("👁️", "OpenCV"),
    ("🤖", "Scikit-learn"),
    ("🧬", "RDKit"),
    ("🌐", "Streamlit"),
    ("📈", "Plotly"),
    ("🔍", "SHAP"),
]

tech_cols = st.columns(len(techs))
for col, (icon, name) in zip(tech_cols, techs):
    with col:
        st.markdown(f"""
        <div style="text-align:center; padding:0.75rem 0.5rem;
                    background:#111827; border:1px solid #1E293B;
                    border-radius:10px;">
          <div style="font-size:1.3rem;">{icon}</div>
          <div style="font-size:0.78rem; color:#94A3B8; margin-top:4px; font-weight:500;">{name}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Core Contributions ────────────────────────────────────────────────────────
section_title("Core Contributions")

contributions = [
    ("✅", "Cellular interaction graph modelling from histology images"),
    ("✅", "Phenotype-based tumour subtype inference via KMeans clustering"),
    ("✅", "Subtype-guided drug ranking using GDSC pharmacogenomics"),
    ("✅", "Pharmacogenomically grounded recommendations — no synthetic supervision"),
    ("✅", "Explainable AI integration: Grad-CAM + SHAP feature attribution"),
]

for icon, text in contributions:
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:12px; padding:0.6rem 0;
                border-bottom:1px solid #1A2235;">
      <span style="color:#00C9A7; font-size:1rem;">{icon}</span>
      <span style="color:#94A3B8; font-size:0.95rem;">{text}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Future Enhancements ───────────────────────────────────────────────────────
section_title("Future Enhancements")

futures = [
    ("🔮", "Graph Attention Visualization", "Extend Grad-CAM to graph attention layers for deeper XAI."),
    ("🌐", "Clinical Validation",           "Validate recommendations against real-world clinical outcomes."),
    ("📏", "Confidence Scoring",            "Add uncertainty estimates to subtype inference predictions."),
    ("🔗", "Multi-Omics Integration",       "Fuse genomic + transcriptomic signals with morphological features."),
]

f1, f2 = st.columns(2)
for i, (icon, title, desc) in enumerate(futures):
    with (f1 if i % 2 == 0 else f2):
        st.markdown(f"""
        <div class="card">
          <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
            <span style="font-size:1.3rem;">{icon}</span>
            <span style="font-weight:600; color:#E2E8F0;">{title}</span>
          </div>
          <p style="color:#64748B; font-size:0.85rem; margin:0; line-height:1.6;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-top:2rem; padding:1.25rem;
            background:linear-gradient(135deg,rgba(0,201,167,0.1),rgba(59,130,246,0.08));
            border:1px solid rgba(0,201,167,0.25); border-radius:12px; color:#00C9A7; font-weight:600;">
  🎓 &nbsp; Developed as part of a Final Year Computer Science Research Project
</div>
""", unsafe_allow_html=True)
