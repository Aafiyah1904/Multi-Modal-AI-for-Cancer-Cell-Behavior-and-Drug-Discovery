import sys
import os

import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import pandas as pd

from utils.styles import inject_styles, page_header, section_title

st.set_page_config(
    page_title="Knowledge Graph – OnchoAI",
    page_icon="🧠",
    layout="wide",
)
inject_styles()

from knowledge_graph.graph_data import build_graph
from knowledge_graph.graph_visualization import visualize_graph
from knowledge_graph.subtype_graph import build_subtype_graph

page_header(
    "🧠",
    "Biological Knowledge Graph",
    "Explore tumour phenotype connections to pathways, genes, and targeted therapies."
)

# Colour legend
st.markdown("""
<div style="display:flex; gap:1.5rem; flex-wrap:wrap; margin-bottom:1.25rem;
            padding:0.75rem 1rem; background:#111827; border:1px solid #1E293B; border-radius:10px;">
  <span style="color:#94A3B8; font-size:0.8rem; font-weight:600; align-self:center;">LEGEND:</span>
  <div style="display:flex; align-items:center; gap:6px;">
    <div style="width:13px; height:13px; border-radius:50%; background:#EF4444;"></div>
    <span style="color:#94A3B8; font-size:0.82rem;">Tumour Subtype</span>
  </div>
  <div style="display:flex; align-items:center; gap:6px;">
    <div style="width:13px; height:13px; border-radius:50%; background:#F59E0B;"></div>
    <span style="color:#94A3B8; font-size:0.82rem;">Biological Pathway</span>
  </div>
  <div style="display:flex; align-items:center; gap:6px;">
    <div style="width:13px; height:13px; border-radius:50%; background:#22C55E;"></div>
    <span style="color:#94A3B8; font-size:0.82rem;">Gene / Biomarker</span>
  </div>
  <div style="display:flex; align-items:center; gap:6px;">
    <div style="width:13px; height:13px; border-radius:50%; background:#3B82F6;"></div>
    <span style="color:#94A3B8; font-size:0.82rem;">Drug / Therapy</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Global graph
section_title("Global Tumour–Drug Network")

G = build_graph()
html_path = visualize_graph(G)
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

st.markdown('<div style="border:1px solid #1E293B; border-radius:12px; overflow:hidden;">', unsafe_allow_html=True)
components.html(html_content, height=620)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown(f"""
<div style="display:flex; gap:1.5rem; margin-top:0.6rem; color:#64748B; font-size:0.82rem;">
  <span>🔵 <strong style="color:#E2E8F0;">{G.number_of_nodes()}</strong> nodes</span>
  <span>🔗 <strong style="color:#E2E8F0;">{G.number_of_edges()}</strong> edges</span>
  <span>🧬 3 subtypes · 6 pathways · 12 genes · 12 drugs</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Subtype-specific graphs with tabs for all 3
section_title("Subtype-Specific Knowledge Graph")

if "predicted_subtype" in st.session_state:
    st.markdown(f"""
    <div style="margin-bottom:1rem;">
      <span class="badge">🧬 Predicted: {st.session_state["predicted_subtype"]}</span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("💡 Run Tumour Analysis first to highlight your predicted subtype.")

tab1, tab2, tab3 = st.tabs(["🟢 Indolent-like", "🟡 Moderate-like", "🔴 Aggressive-like"])

for subtype_name, tab in zip(
    ["Indolent-like", "Moderate-like", "Aggressive-like"],
    [tab1, tab2, tab3]
):
    with tab:
        G2 = build_subtype_graph(subtype_name)
        hp = visualize_graph(G2)
        with open(hp, "r", encoding="utf-8") as f:
            hc = f.read()
        st.markdown('<div style="border:1px solid #1E293B; border-radius:12px; overflow:hidden;">', unsafe_allow_html=True)
        components.html(hc, height=500)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="color:#64748B; font-size:0.82rem; margin-top:0.5rem;">
          {G2.number_of_nodes()} nodes · {G2.number_of_edges()} edges
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Heatmap
section_title("Subtype–Drug Compatibility Landscape")

st.markdown("""
<p style="color:#64748B; font-size:0.9rem; margin-bottom:0.5rem;">
  Drug compatibility scores derived from GDSC pharmacogenomic data.
  Scores are <strong style="color:#E2E8F0;">globally normalized</strong> —
  comparable across all subtypes. The dashed red line marks the predicted subtype.
</p>
""", unsafe_allow_html=True)

with st.expander("ℹ️  How to read this heatmap", expanded=False):
    st.markdown("""
    - **Rows** — drugs ranked via GDSC pharmacogenomic sensitivity data.
    - **Columns** — tumour phenotype subtypes.
    - **Color intensity** — compatibility score (higher = better effectiveness).
    - **Globally normalized** — scores are comparable across subtypes.
    - **Dashed red line** — the subtype predicted for your uploaded image.
    """)

try:
    drug_data = pd.read_csv("../outputs/drug_ranking/subtype_specific_drug_ranking.csv")

    top_drugs = (
        drug_data.groupby("Drug Name")["Compatibility Score"]
        .mean().sort_values(ascending=False).head(12).index
    )

    pivot_table = drug_data[drug_data["Drug Name"].isin(top_drugs)].pivot(
        index="Drug Name", columns="Subtype", values="Compatibility Score"
    )

    fig = px.imshow(
        pivot_table, text_auto=".2f",
        color_continuous_scale="viridis", aspect="auto",
        title="Drug Compatibility Across Tumour Subtypes",
    )
    fig.update_layout(
        height=680,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#E2E8F0", xaxis_title="Tumour Subtype", yaxis_title="Drug",
        title_font_size=14,
        coloraxis_colorbar=dict(bgcolor="rgba(0,0,0,0)", tickfont=dict(color="#E2E8F0")),
    )

    if "predicted_subtype" in st.session_state:
        cols_list = list(pivot_table.columns)
        pred = st.session_state["predicted_subtype"]
        if pred in cols_list:
            fig.add_vline(x=cols_list.index(pred), line_width=3, line_dash="dash", line_color="#EF4444")

    st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.warning("⚠️  Drug ranking CSV not found. Re-run phase6 notebook first.")