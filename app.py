import streamlit as st
import pandas as pd
import numpy as np
import pdfplumber
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import time
import random
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- 1. APP CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="SkillSetu AI | Enterprise Edition",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enterprise CSS
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #FAFAFA;
    }
    
    /* Card Styling */
    .css-1r6slb0 {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        color: #004d99;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Segoe UI', sans-serif;
        color: #1a1a1a;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #0052cc 0%, #003380 100%);
        color: white;
        border: none;
        border-radius: 8px;
        height: 50px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,82,204,0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- 2. ADVANCED AI ENGINES (FUNCTIONS) ---

def extract_text(feed):
    """Robust PDF Text Extraction"""
    text = ""
    with pdfplumber.open(feed) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def compute_similarity(text1, text2):
    """
    Calculates Cosine Similarity using TF-IDF Vectors.
    This is mathematically superior to simple keyword matching.
    """
    # Clean text
    clean_t1 = re.sub(r'[^\w\s]', '', text1.lower())
    clean_t2 = re.sub(r'[^\w\s]', '', text2.lower())
    
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([clean_t1, clean_t2])
    
    # Calculate Cosine Similarity (0 to 1)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(similarity * 100, 2)

def generate_skill_graph(role):
    """Generates a directed graph for learning paths based on role"""
    G = nx.DiGraph()
    
    if role == "Data Scientist":
        edges = [('Python', 'Pandas'), ('Pandas', 'Data Viz'), ('Data Viz', 'Statistics'), 
                 ('Statistics', 'Machine Learning'), ('Machine Learning', 'Deep Learning')]
    elif role == "Full Stack Dev":
        edges = [('HTML/CSS', 'JavaScript'), ('JavaScript', 'React'), ('React', 'Node.js'), 
                 ('Node.js', 'MongoDB'), ('MongoDB', 'Deployment')]
    else:
        edges = [('Basics', 'Intermediate'), ('Intermediate', 'Advanced'), ('Advanced', 'Expert')]
        
    G.add_edges_from(edges)
    return G

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2083/2083236.png", width=80)
    st.title("SkillSetu AI")
    st.caption("Enterprise Edition v2.4")
    st.markdown("---")
    
    menu = st.radio("Navigation", [
        "📊 Executive Dashboard", 
        "🧠 AI Resume Architect", 
        "🕸️ Skill Knowledge Graph", 
        "💼 Job Market Intelligence", 
        "🤖 Interview Simulator"
    ])
    
    st.markdown("---")
    st.info("💡 **Pro Tip:** Upload a PDF to unlock deep analytics.")

# --- 4. PAGE LOGIC ---

# === PAGE: DASHBOARD ===
if menu == "📊 Executive Dashboard":
    st.title("🇮🇳 National Skill & Employment Overview")
    st.markdown("Real-time telemetry from 28 States and 8 UTs.")
    
    # Top Metrics Row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Active Job Seekers", "4.2M", "12% ▲")
    c2.metric("Placements (Today)", "1,240", "5% ▲")
    c3.metric("Skill Gap Index", "34%", "-2% ▼")
    c4.metric("Avg. Salary Hike", "18%", "Stable")
    
    # Interactive Map (Using Plotly)
    st.subheader("📍 Live Hiring Heatmap")
    
    # Mock Data for Map
    data = pd.DataFrame({
        'City': ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Pune'],
        'Lat': [19.0760, 28.7041, 12.9716, 17.3850, 13.0827, 18.5204],
        'Lon': [72.8777, 77.1025, 77.5946, 78.4867, 80.2707, 73.8567],
        'Jobs': [1500, 1200, 2500, 1800, 1100, 900],
        'Demand': ['High', 'High', 'Critical', 'High', 'Moderate', 'Moderate']
    })
    
    fig = px.scatter_mapbox(data, lat="Lat", lon="Lon", size="Jobs", color="Demand",
                            color_discrete_map={'Critical': 'red', 'High': 'orange', 'Moderate': 'blue'},
                            zoom=3.5, mapbox_style="carto-positron", height=500,
                            hover_name="City", size_max=40)
    st.plotly_chart(fig, use_container_width=True)

# === PAGE: AI RESUME ARCHITECT ===
elif menu == "🧠 AI Resume Architect":
    st.header("🧠 Neural Resume Analyzer")
    st.markdown("Uses **TF-IDF Vectorization** & **Cosine Similarity** to match candidates.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1. Candidate Profile")
        uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
        
    with col2:
        st.subheader("2. Target Role Description")
        jd = st.text_area("Paste JD Here", height=200, 
                          placeholder="e.g. Seeking Python developer with Flask and AWS experience...")

    if uploaded_file and jd:
        with st.spinner("Initializing Neural Network Analysis..."):
            time.sleep(1.5) # UX Delay
            resume_text = extract_text(uploaded_file)
            score = compute_similarity(resume_text, jd)
            
        # --- RESULTS SECTION ---
        st.markdown("---")
        
        # Donut Chart for Score
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            title = {'text': "AI Match Confidence"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#0052cc"},
                'steps': [
                    {'range': [0, 50], 'color': "#ffe6e6"},
                    {'range': [50, 75], 'color': "#fff5e6"},
                    {'range': [75, 100], 'color': "#e6ffee"}
                ],
            }
        ))
        
        c1, c2 = st.columns([1, 2])
        with c1:
            st.plotly_chart(fig_gauge, use_container_width=True)
            
        with c2:
            st.subheader("🔍 Analysis Report")
            if score > 75:
                st.success("✅ **High Probability Match:** Your semantic profile aligns well with the job.")
            elif score > 50:
                st.warning("⚠️ **Moderate Match:** You have the basics, but lack specific technical keywords found in the JD.")
            else:
                st.error("❌ **Low Match:** Significant skill gap detected. AI Recommendation: Upskill immediately.")
                
            with st.expander("View Extracted Resume Text"):
                st.text(resume_text[:500] + "...")

# === PAGE: SKILL GRAPH ===
elif menu == "🕸️ Skill Knowledge Graph":
    st.header("🕸️ Interactive Learning Path")
    st.markdown("Visualizing the *dependency tree* of technical skills.")
    
    role = st.selectbox("Select Career Path", ["Data Scientist", "Full Stack Dev", "DevOps Engineer"])
    
    if st.button("Generate Graph"):
        G = generate_skill_graph(role)
        
        # Create positions for the nodes
        pos = nx.spring_layout(G)
        
        # Extract node and edge coordinates for Plotly
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=2, color='#888'), hoverinfo='none', mode='lines')

        node_x = []
        node_y = []
        node_text = []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)

        node_trace = go.Scatter(
            x=node_x, y=node_y, mode='markers+text',
            text=node_text, textposition="top center",
            marker=dict(showscale=True, colorscale='YlGnBu', size=30, color=[1, 2, 3, 4, 5], line_width=2)
        )

        fig = go.Figure(data=[edge_trace, node_trace],
                     layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0,l=0,r=0,t=0),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                     )
        
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Nodes represent skills. Arrows represent the learning prerequisite order.")

# === PAGE: MARKET INTEL ===
elif menu == "💼 Job Market Intelligence":
    st.header("💼 Predictive Market Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Salary Trend Prediction")
        # Fake Linear Regression Visual
        x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
        y = np.array([3.5, 4.2, 5.8, 7.1, 10.5, 12.0, 15.5, 18.0])
        
        df_sal = pd.DataFrame({'Years Experience': x, 'Salary (LPA)': y})
        fig = px.scatter(df_sal, x='Years Experience', y='Salary (LPA)', trendline="ols", 
                         title="Salary vs Experience (Linear Regression Model)")
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("Top Skills Demand (Real-time)")
        df_skills = pd.DataFrame({
            'Skill': ['Python', 'SQL', 'AWS', 'React', 'Docker'],
            'Openings': [4500, 3800, 3200, 2900, 2100]
        })
        fig2 = px.bar(df_skills, x='Skill', y='Openings', color='Openings', 
                      color_continuous_scale='Viridis')
        st.plotly_chart(fig2, use_container_width=True)

# === PAGE: INTERVIEW SIMULATOR ===
elif menu == "🤖 Interview Simulator":
    st.header("🤖 AI Mock Interviewer")
    st.write("Practicing for: **Data Science Role**")
    
    # Simple Chat Interface using Session State
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! I am your AI Interviewer. Let's start with a basic question: Tell me about a time you handled a difficult project?"}]

    # Display Chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # User Input
    if prompt := st.chat_input("Type your answer here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
            
        # Simulate AI Thinking
        with st.spinner("AI is analyzing your sentiment and confidence..."):
            time.sleep(1.5)
            
        # Hardcoded logic for demo
        ai_response = "That's a solid example. You used the STAR method (Situation, Task, Action, Result). However, try to quantify the result more—did efficiency increase by 10% or 50%?"
        
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        with st.chat_message("assistant"):
            st.write(ai_response)
