"""
Shared UI styles and components for the AI Tumour Analysis Platform.
Import this in every page: from utils.styles import inject_styles, page_header
"""

import streamlit as st


GLOBAL_CSS = """
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

/* ── Root Variables ── */
:root {
    --teal:      #00C9A7;
    --teal-dim:  #00a88a;
    --blue:      #3B82F6;
    --purple:    #8B5CF6;
    --red:       #EF4444;
    --amber:     #F59E0B;
    --bg:        #0A0E1A;
    --surface:   #111827;
    --surface2:  #1A2235;
    --border:    #1E293B;
    --text:      #E2E8F0;
    --muted:     #64748B;
    --radius:    12px;
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Hide Streamlit Branding ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1220 0%, #111827 100%) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] span {
    color: var(--text) !important;
}
[data-testid="stSidebarNav"] a {
    border-radius: 8px;
    margin: 2px 0;
    transition: background 0.2s;
}
[data-testid="stSidebarNav"] a:hover {
    background: var(--surface2) !important;
}
[data-testid="stSidebarNav"] a[aria-selected="true"] {
    background: rgba(0,201,167,0.15) !important;
    border-left: 3px solid var(--teal) !important;
}

/* ── Main Content Area ── */
.block-container {
    padding: 2rem 3rem !important;
    max-width: 1200px !important;
}

/* ── Headings ── */
h1 { font-size: 2rem !important; font-weight: 700 !important; letter-spacing: -0.5px !important; }
h2 { font-size: 1.4rem !important; font-weight: 600 !important; }
h3 { font-size: 1.1rem !important; font-weight: 600 !important; }

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--teal) 0%, #009e84 100%) !important;
    color: #0A0E1A !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.3px !important;
    padding: 0.65rem 1.5rem !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
    box-shadow: 0 4px 15px rgba(0,201,167,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(0,201,167,0.4) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── File Uploader ── */
[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 2px dashed var(--border) !important;
    border-radius: var(--radius) !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--teal) !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1rem 1.2rem !important;
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 0.8rem !important; }
[data-testid="stMetricValue"] { color: var(--teal) !important; font-size: 1.6rem !important; font-weight: 700 !important; }

/* ── Info / Success / Warning / Error ── */
.stAlert {
    border-radius: var(--radius) !important;
    border-left-width: 4px !important;
}
[data-baseweb="notification"][kind="info"] {
    background: rgba(59,130,246,0.1) !important;
    border-left-color: var(--blue) !important;
}
[data-baseweb="notification"][kind="success"] {
    background: rgba(0,201,167,0.1) !important;
    border-left-color: var(--teal) !important;
}
[data-baseweb="notification"][kind="warning"] {
    background: rgba(245,158,11,0.1) !important;
    border-left-color: var(--amber) !important;
}
[data-baseweb="notification"][kind="error"] {
    background: rgba(239,68,68,0.1) !important;
    border-left-color: var(--red) !important;
}

/* ── DataFrames ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    overflow: hidden !important;
}

/* ── Progress Bar ── */
[data-baseweb="progress-bar"] > div {
    background: linear-gradient(90deg, var(--teal), var(--blue)) !important;
    border-radius: 999px !important;
}
[data-baseweb="progress-bar"] {
    background: var(--surface2) !important;
    border-radius: 999px !important;
    height: 6px !important;
}

/* ── Tabs ── */
[data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: var(--radius) !important;
    padding: 4px !important;
    gap: 4px !important;
}
[data-baseweb="tab"] {
    border-radius: 8px !important;
    color: var(--muted) !important;
    font-weight: 500 !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    background: var(--surface2) !important;
    color: var(--teal) !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--teal) !important; }

/* ── Custom Card ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s, transform 0.2s;
}
.card:hover { border-color: rgba(0,201,167,0.4); transform: translateY(-2px); }

/* ── Teal Gradient Badge ── */
.badge {
    display: inline-block;
    background: rgba(0,201,167,0.15);
    color: var(--teal);
    border: 1px solid rgba(0,201,167,0.3);
    border-radius: 999px;
    padding: 3px 12px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}

/* ── Pipeline Step ── */
.pipeline-step {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem;
    text-align: center;
    position: relative;
}
.pipeline-step .step-icon { font-size: 1.8rem; margin-bottom: 0.5rem; }
.pipeline-step .step-title { font-weight: 600; font-size: 0.9rem; color: var(--text); }
.pipeline-step .step-desc { color: var(--muted); font-size: 0.78rem; margin-top: 0.25rem; }

/* ── Plotly chart background ── */
.js-plotly-plot .plotly .bg { fill: transparent !important; }

/* ── Monospace for code/labels ── */
.mono { font-family: 'IBM Plex Mono', monospace !important; }

/* ── Glow effect for prediction result ── */
.prediction-banner {
    background: linear-gradient(135deg, rgba(0,201,167,0.15) 0%, rgba(59,130,246,0.1) 100%);
    border: 1px solid rgba(0,201,167,0.4);
    border-radius: var(--radius);
    padding: 1rem 1.5rem;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--teal);
    text-align: center;
    margin: 1rem 0;
    box-shadow: 0 0 30px rgba(0,201,167,0.1);
}
</style>
"""


SIDEBAR_LOGO = """
<div style="padding: 1.2rem 1rem 0.5rem; border-bottom: 1px solid #1E293B; margin-bottom: 1rem;">
  <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
    <span style="font-size:1.6rem;">🧬</span>
    <div>
      <div style="font-weight:700; font-size:1rem; color:#E2E8F0; line-height:1.2;">OnchoAI</div>
      <div style="font-size:0.72rem; color:#64748B; letter-spacing:0.5px;">TUMOUR ANALYSIS PLATFORM</div>
    </div>
  </div>
</div>
"""


def inject_styles():
    """Inject global CSS + sidebar logo into every page."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.sidebar.markdown(SIDEBAR_LOGO, unsafe_allow_html=True)


def page_header(icon: str, title: str, subtitle: str = ""):
    """Render a consistent page header."""
    st.markdown(f"""
    <div style="margin-bottom:1.5rem;">
      <div style="display:flex; align-items:center; gap:12px; margin-bottom:6px;">
        <span style="font-size:2rem;">{icon}</span>
        <h1 style="margin:0; font-size:1.9rem; font-weight:700; color:#E2E8F0;">{title}</h1>
      </div>
      {"<p style='color:#64748B; margin:0; font-size:0.95rem; padding-left:3.2rem;'>" + subtitle + "</p>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)


def section_title(text: str):
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:10px; margin:1.5rem 0 0.75rem;">
      <div style="width:3px; height:20px; background: linear-gradient(180deg,#00C9A7,#3B82F6); border-radius:2px;"></div>
      <h3 style="margin:0; font-size:1.05rem; font-weight:600; color:#E2E8F0;">{text}</h3>
    </div>
    """, unsafe_allow_html=True)


def drug_card(drug_name: str, score: float, rank: int):
    """Render a styled drug recommendation card."""
    bar_pct = min(int(score * 100), 100)
    color = "#00C9A7" if score > 0.7 else "#3B82F6" if score > 0.4 else "#8B5CF6"
    st.markdown(f"""
    <div class="card" style="display:flex; align-items:center; gap:1rem;">
      <div style="min-width:48px; height:48px; border-radius:50%; background:rgba(0,201,167,0.12);
                  border:2px solid rgba(0,201,167,0.3); display:flex; align-items:center;
                  justify-content:center; font-weight:700; color:#00C9A7; font-size:0.9rem;">
        #{rank}
      </div>
      <div style="flex:1;">
        <div style="font-weight:600; font-size:1rem; color:#E2E8F0; margin-bottom:4px;">{drug_name}</div>
        <div style="background:#1A2235; border-radius:999px; height:6px; overflow:hidden;">
          <div style="width:{bar_pct}%; height:100%; background:linear-gradient(90deg,{color},{color}aa); border-radius:999px;"></div>
        </div>
        <div style="color:#64748B; font-size:0.78rem; margin-top:4px;">Compatibility Score: <span style="color:{color}; font-weight:600;">{score:.3f}</span></div>
      </div>
    </div>
    """, unsafe_allow_html=True)
