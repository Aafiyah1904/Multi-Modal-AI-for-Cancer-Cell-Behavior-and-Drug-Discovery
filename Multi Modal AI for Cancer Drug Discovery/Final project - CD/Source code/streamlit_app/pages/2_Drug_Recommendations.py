import sys
import os

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.styles import inject_styles, page_header, section_title, drug_card

st.set_page_config(
    page_title="Drug Recommendations – OnchoAI",
    page_icon="💊",
    layout="wide",
)
inject_styles()

page_header(
    "💊",
    "Drug Recommendations",
    "Candidate drugs ranked by predicted tumour phenotype compatibility."
)

# ── Guard ─────────────────────────────────────────────────────────────────────
if "predicted_subtype" not in st.session_state:
    st.warning("⚠️  No analysis found. Please run Tumour Analysis first.")
    if st.button("Go to Tumour Analysis"):
        st.switch_page("pages/1_Tumour_Analysis.py")
    st.stop()

subtype = st.session_state["predicted_subtype"]
drugs   = st.session_state["recommended_drugs"]

# Subtype banner
subtype_colors = {
    "Aggressive-like": "#EF4444",
    "Moderate-like":   "#F59E0B",
    "Indolent-like":   "#00C9A7",
}
sc = subtype_colors.get(subtype, "#3B82F6")
st.markdown(f"""
<div style="background:rgba({int(sc[1:3],16)},{int(sc[3:5],16)},{int(sc[5:7],16)},0.12);
            border:1px solid {sc}55; border-left: 4px solid {sc};
            border-radius:12px; padding:1rem 1.5rem; margin-bottom:1.5rem;
            display:flex; align-items:center; gap:12px;">
  <span style="font-size:1.4rem;">🧬</span>
  <div>
    <div style="color:#94A3B8; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.5px;">Predicted Subtype</div>
    <div style="font-size:1.15rem; font-weight:700; color:{sc};">{subtype}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Pipeline Steps ────────────────────────────────────────────────────────────
section_title("Drug Recommendation Pipeline")

steps = [
    ("🔬", "Phenotype Detection",   "CNN + GNN identifies tumour subtype from histology."),
    ("🗺️", "Phenotype–Drug Mapping", "Subtype mapped to pharmacogenomic therapeutic targets."),
    ("📊", "Drug Ranking Model",    "Candidates ranked using GDSC IC50 sensitivity data."),
    ("💊", "Top Candidates",        "Highest-ranked therapies returned for this phenotype."),
]
cols = st.columns(4)
for col, (icon, title, desc) in zip(cols, steps):
    with col:
        st.markdown(f"""
        <div class="pipeline-step">
          <div class="step-icon">{icon}</div>
          <div class="step-title">{title}</div>
          <div class="step-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Guard: empty drugs ────────────────────────────────────────────────────────
if drugs is None or drugs.empty:
    st.error("No drug recommendations found. Please re-run tumour analysis.")
    st.stop()

# ── Score column detection ────────────────────────────────────────────────────
score_column = None
for col in drugs.columns:
    if col.lower() in ["score", "ranking", "rank", "value", "effectiveness"]:
        score_column = col
        break
if score_column is None:
    drugs["Rank"] = range(1, len(drugs) + 1)
    score_column = "Rank"

drugs = drugs.sort_values(by=score_column, ascending=False).reset_index(drop=True)
drug_name_col = "Drug" if "Drug" in drugs.columns else drugs.columns[0]

# ── Drug Cards ────────────────────────────────────────────────────────────────
section_title(f"Ranked Candidates for {subtype}")

top5_drugs = drugs.head(5)

for idx, row in top5_drugs.iterrows():
    try:
        score_val = float(row[score_column])
    except Exception:
        score_val = 0.0
    drug_card(row[drug_name_col], score_val, idx + 1)

st.markdown("<br>", unsafe_allow_html=True)

# ── Bar Chart ─────────────────────────────────────────────────────────────────
section_title("Effectiveness Ranking Chart")

fig = px.bar(
    drugs,
    x=drug_name_col,
    y=score_column,
    color=score_column,
    color_continuous_scale=[[0, "#8B5CF6"], [0.5, "#3B82F6"], [1, "#00C9A7"]],
    title=f"Drug Ranking – {subtype}",
)
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#E2E8F0",
    xaxis=dict(gridcolor="#1E293B", tickangle=-35, title="Drug"),
    yaxis=dict(gridcolor="#1E293B", title="Score"),
    coloraxis_showscale=False,
    title_font_size=14,
)
st.plotly_chart(fig, use_container_width=True)

# ── Full Table ────────────────────────────────────────────────────────────────
section_title("Top 20 Drug Candidates")

st.dataframe(
    drugs.head(20),
    use_container_width=True,
    hide_index=True
)