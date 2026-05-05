import sys
import os
from pathlib import Path

# ── Add streamlit_app/ AND Final_Year_Project/ (parent) to sys.path ──────────
_ROOT        = Path(__file__).resolve().parent   # .../streamlit_app/
_PARENT_ROOT = _ROOT.parent                      # .../Final_Year_Project/
for _p in [str(_ROOT), str(_PARENT_ROOT)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

import streamlit as st

st.set_page_config(
    page_title="OnchoAI – Tumour Analysis Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.styles import inject_styles
inject_styles()

st.markdown("""
<div style="text-align:center; padding: 3rem 1rem 2rem;">
  <div style="font-size:3.5rem; margin-bottom:1rem;">🧬</div>
  <h1 style="font-size:2.6rem; font-weight:700; margin:0; background:linear-gradient(135deg,#00C9A7,#3B82F6);
             -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">
    OnchoAI
  </h1>
  <p style="color:#64748B; font-size:1.1rem; margin:0.5rem 0 0; letter-spacing:0.5px;">
    AI-Powered Tumour Analysis &amp; Drug Discovery Platform
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("""
<p style="text-align:center; color:#94A3B8; font-size:1rem; max-width:720px;
           margin:0 auto 2.5rem; line-height:1.7;">
  This system integrates <strong style="color:#E2E8F0;">deep learning</strong>,
  <strong style="color:#E2E8F0;">graph neural networks</strong>, and
  <strong style="color:#E2E8F0;">explainable AI</strong> to analyse histopathology
  images and recommend candidate anti-cancer drugs — grounded in real pharmacogenomic data.
</p>
""", unsafe_allow_html=True)

steps = [
    ("📷", "Image Upload",          "Accepts histopathology PNG/JPG slides"),
    ("🧠", "CNN Feature Extraction", "ResNet-18 extracts morphological features"),
    ("🔗", "Cellular Graph",         "Spatial nuclear interactions modelled as graphs"),
    ("📡", "Graph Neural Network",   "GCN encodes structural tumour behaviour"),
    ("🔬", "Phenotype Prediction",   "KMeans clustering infers tumour subtype"),
    ("💊", "Drug Recommendation",    "GDSC pharmacogenomic ranking per subtype"),
]

cols = st.columns(3)
for i, (icon, title, desc) in enumerate(steps):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="pipeline-step" style="margin-bottom:1rem;">
          <div class="step-icon">{icon}</div>
          <div class="step-title">{title}</div>
          <div class="step-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

col_l, col_m, col_r = st.columns([1, 2, 1])
with col_m:
    if st.button("🔬  Start Tumour Analysis", use_container_width=True):
        st.switch_page("pages/1_Tumour_Analysis.py")

st.markdown("""
<div style="text-align:center; margin-top:3rem; padding-top:1.5rem;
            border-top:1px solid #1E293B; color:#334155; font-size:0.8rem;">
  Final Year Research Project · AI-Driven Cancer Drug Discovery
</div>
""", unsafe_allow_html=True)