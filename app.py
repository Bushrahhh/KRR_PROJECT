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
    
    st.header("📁 Data Source")
    rdf_path = st.text_input("RDF file name", value=DEFAULT_PATH.name)
    rdf_file = BASE_DIR / rdf_path
    
    st.divider()
    
    if st.button("📊 Load File", type="primary", use_container_width=True):
        st.session_state['load_file'] = True
    
    st.divider()
    
    with st.expander("ℹ️ About"):
        st.write("""
        **Project Baba** - Simple RDF Explorer
        
        Just upload your RDF file and start querying.
        Works with: RDF/XML, Turtle, N-Triples, N3
        """)

# ---------------------------------------------------
# Main Content
# ---------------------------------------------------
# Load graph when button is clicked
if 'load_file' in st.session_state and st.session_state['load_file']:
    try:
        with st.spinner('Loading RDF file...'):
            g = load_graph(rdf_file)
            st.session_state['graph'] = g
            st.session_state['file_loaded'] = True
            
            st.success(f"✅ Successfully loaded **{len(g):,} triples**")
            
            # Show stats in columns
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Triples", f"{len(g):,}")
            with col2:
                st.metric("Unique Subjects", f"{len(set(g.subjects())):,}")
            with col3:
                st.metric("Predicates", f"{len(set(g.predicates())):,}")
                
            # Show first few predicates
            with st.expander("📋 Show Predicates (first 50)"):
                preds = sorted(set(str(p) for p in g.predicates()))
                for i, pred in enumerate(preds[:50]):
                    st.code(pred)
                if len(preds) > 50:
                    st.info(f"... and {len(preds) - 50} more predicates")
                    
    except Exception as e:
        st.error(f"❌ Failed to load file: {str(e)}")
        st.session_state['file_loaded'] = False

# Show message if no file loaded yet
elif 'file_loaded' not in st.session_state:
    st.info("👈 Click 'Load File' in the sidebar to start")

# ---------------------------------------------------
# SPARQL Query Interface
# ---------------------------------------------------
if 'file_loaded' in st.session_state and st.session_state['file_loaded']:
    st.divider()
    st.subheader("🔍 SPARQL Query Console")
    
    # Query templates
    template_cols = st.columns(3)
    with template_cols[0]:
        if st.button("Get All Triples", use_container_width=True):
            st.session_state['query_text'] = "SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 50"
    with template_cols[1]:
        if st.button("Find Resources", use_container_width=True):
            st.session_state['query_text'] = "SELECT DISTINCT ?s WHERE { ?s ?p ?o } LIMIT 50"
    with template_cols[2]:
        if st.button("Count Predicates", use_container_width=True):
            st.session_state['query_text'] = """SELECT ?p (COUNT(?p) as ?count) 
WHERE { ?s ?p ?o } 
GROUP BY ?p 
ORDER BY DESC(?count) 
LIMIT 20"""
    
    # Text area for query
    default_query = st.session_state.get('query_text', """SELECT ?s ?p ?o 
WHERE {
    ?s ?p ?o
}
LIMIT 50""")
    
    query = st.text_area("Enter SPARQL Query:", 
                        value=default_query, 
                        height=200,
                        placeholder="Write your SPARQL query here...")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        run_query = st.button("🚀 Run Query", type="primary", use_container_width=True)
    
    if run_query:
        try:
            g = st.session_state['graph']
            results = g.query(query)
            
            # Convert to DataFrame
            rows = []
            for r in results:
                rows.append([str(x) for x in r])
            
            if rows:
                df = pd.DataFrame(rows, columns=[str(v) for v in results.vars])
                
                st.success(f"✅ Query returned {len(df)} rows")
                
                # Display results
                st.dataframe(df, use_container_width=True, height=400)
                
                # Download buttons
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Download as CSV",
                    csv,
                    f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv",
                    key='download-csv'
                )
            else:
                st.info("Query executed successfully but returned no results.")
                
        except Exception as e:
            st.error(f"Query failed: {str(e)}")

# ---------------------------------------------------
# Quick Analysis Section
# ---------------------------------------------------
if 'file_loaded' in st.session_state and st.session_state['file_loaded']:
    st.divider()
    st.subheader("📊 Quick Analysis")
    
    if st.button("Run Quick Analysis", type="secondary"):
        g = st.session_state['graph']
        
        # Basic stats
        subjects = list(g.subjects())
        predicates = list(g.predicates())
        objects = list(g.objects())
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Triples", len(g))
        with col2:
            st.metric("Unique Subjects", len(set(subjects)))
        with col3:
            st.metric("Unique Predicates", len(set(predicates)))
        with col4:
            st.metric("Unique Objects", len(set(objects)))
        
        # Most common predicates
        st.subheader("📈 Most Common Predicates")
        pred_counts = {}
        for p in predicates:
            p_str = str(p)
            # Shorten long URIs
            if '#' in p_str:
                p_short = p_str.split('#')[-1]
            elif '/' in p_str:
                p_short = p_str.split('/')[-1]
            else:
                p_short = p_str
            
            pred_counts[p_short] = pred_counts.get(p_short, 0) + 1
        
        # Show top 10
        top_preds = sorted(pred_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        if top_preds:
            pred_df = pd.DataFrame(top_preds, columns=['Predicate', 'Count'])
            st.dataframe(pred_df, use_container_width=True)

# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.markdown("---")
st.caption(f"🔮 Project Baba • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} • Ready")