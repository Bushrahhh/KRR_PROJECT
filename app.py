import streamlit as st
import pandas as pd
from rdflib import Graph
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------
# Page setup with cool styling
# ---------------------------------------------------
st.set_page_config(
    page_title="Project Baba - RDF Explorer",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem !important;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem !important;
        font-weight: 900;
    }
    
    .sub-header {
        text-align: center;
        color: #94A3B8;
        font-size: 1.2rem;
        margin-bottom: 2rem !important;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1E293B, #0F172A);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #3B82F6;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #1E293B;
        border-radius: 8px 8px 0 0;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3B82F6 !important;
    }
    
    .custom-sidebar {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
        padding: 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Project Header
# ---------------------------------------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<h1 class="main-header">🔮 PROJECT BABA</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">RDF Knowledge Graph Explorer | Simple & Fast</p>', unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------
# File location (Windows-safe)
# ---------------------------------------------------
BASE_DIR = Path(__file__).parent
DEFAULT_PATH = BASE_DIR / "Fictional_Characters_V5.rdf"

# ---------------------------------------------------
# Load RDF Graph
# ---------------------------------------------------
@st.cache_data
def load_graph(rdf_path: Path) -> Graph:
    g = Graph()
    
    # Try formats automatically
    for fmt in ["xml", "turtle", "nt", "n3"]:
        try:
            g.parse(rdf_path.as_posix(), format=fmt)
            return g
        except Exception:
            continue
    
    raise Exception("Could not parse RDF file with known formats.")

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------
with st.sidebar:
    st.markdown('<div class="custom-sidebar">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 4rem; margin-bottom: 0.5rem;">🔮</div>
        <h3 style="color: #3B82F6;">PROJECT BABA</h3>
        <p style="color: #94A3B8; font-size: 0.9rem;">Simple RDF Explorer v1.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.header("📁 D