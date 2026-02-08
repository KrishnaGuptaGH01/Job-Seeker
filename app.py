import streamlit as st
import time
import pandas as pd
import random

# Page Configuration
st.set_page_config(
    page_title="SkillSetu AI",
    page_icon="🇮🇳",
    layout="wide"
)

# Custom Styling to look like a Government/Official Portal
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        background-color: #FF9933;
        color: white;
        border-radius: 10px;
        width: 100%;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("SkillSetu AI 🇮🇳")
page = st.sidebar.radio("Navigate", ["🏠 Home", "🚀 Career & Upskilling", "🏗️ Blue Collar Jobs", "📊 Gov Dashboard"])

st.sidebar.markdown("---")
st.sidebar.info("Category: Skill Development\nStatus: Prototype")

# --- HOME PAGE ---
if page == "🏠 Home":
    st.title("SkillSetu AI: Bridging Talent & Opportunity")
    st.markdown("### Empowering India's Workforce with AI-Driven Guidance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("https://img.freepik.com/free-vector/job-hunt-concept-illustration_114360-423.jpg", width=400)
    
    with col2:
        st.write("""
        **The Problem:** Unemployment isn't just about lack of jobs; it's about the *Skill Gap*.
        
        **Our Solution:**
        * **For Students:** AI Resume Analysis & Gap Mapping.
        * **For Workers:** Local Gig Matching (Vernacular).
        * **For Govt:** Real-time Skilling Dashboards.
        """)
        st.warning("⚡ Live Market Data: 14,203 Jobs available in your region today.")

# --- CAREER & UPSKILLING (The AI Demo) ---
elif page == "🚀 Career & Upskilling":
    st.header("🤖 AI Career Compass")
    st.write("Upload your resume or enter details to find your skill gap.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        name = st.text_input("Full Name")
        role = st.selectbox("Target Role", ["Data Scientist", "Full Stack Developer", "Digital Marketer"])
        skills = st.multiselect("Your Current Skills", ["Python", "Java", "React", "Excel", "Communication", "SQL"])
        
        if st.button("Analyze Profile"):
            if not name:
                st.error("Please enter your name.")
            else:
                with st.spinner('AI is scanning 50,000+ job descriptions...'):
                    time.sleep(2) # Fake processing time
                
                st.success(f"Analysis Complete for {name}!")
                
                # Logic for the Demo
                if "React" not in skills and role == "Full Stack Developer":
                    gap = "React.js"
                    course = "Meta Front-End Developer Certificate"
                elif "Python" not in skills and role == "Data Scientist":
                    gap = "Python & Statistics"
                    course = "Google Data Analytics Professional Certificate"
                else:
                    gap = "Advanced System Design"
                    course = "System Design Interview Prep"
                
                st.session_state['result'] = {
                    "gap": gap,
                    "course": course,
                    "score": random.randint(65, 85)
                }

    with col2:
        if 'result' in st.session_state:
            res = st.session_state['result']
            st.markdown(f"""
            ### 📄 Profile Report
            
            **Employability Score:** {res['score']}/100
            
            **⚠️ CRITICAL SKILL GAP IDENTIFIED:**
            The market demands **{res['gap']}** for this role, but it is missing from your profile.
            
            **💡 AI RECOMMENDATION:**
            We have found a sponsored course for you:
            * **Course:** {res['course']}
            * **Duration:** 4 Weeks
            * **Outcome:** Guaranteed Interview with 3 Local Startups.
            """)
            st.progress(res['score'])
            st.button("Enroll Now (Free under Skill India)")

# --- BLUE COLLAR JOBS ---
elif page == "🏗️ Blue Collar Jobs":
    st.header("📍 Local Sahayak (Helper)")
    st.write("Voice-enabled job finding for skilled trades.")
    
    st.info("🎙️ Voice Search Active (Click to Speak - Simulation)")
    
    loc = st.text_input("Enter Your Pincode", "462001")
    
    if st.button("Find Work Nearby"):
        st.write(f"Searching in **{loc}**...")
        time.sleep(1)
        
        jobs = [
            {"Role": "Electrician", "Pay": "₹800/day", "Dist": "1.2 km"},
            {"Role": "Plumber", "Pay": "₹600/visit", "Dist": "2.5 km"},
            {"Role": "Carpenter", "Pay": "₹1200/day", "Dist": "0.8 km"},
        ]
        
        df = pd.DataFrame(jobs)
        st.table(df)
        st.map(pd.DataFrame({'lat': [23.25], 'lon': [77.41]})) # Centered on Bhopal

# --- GOV DASHBOARD ---
elif page == "📊 Gov Dashboard":
    st.header("🇮🇳 National Skilling Dashboard")
    st.write("Real-time analytics for Government Officers.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Youth Enrolled", "1,240,500", "+12%")
    col2.metric("Placement Rate", "68%", "+5%")
    col3.metric("Top Skill Demand", "Solar Tech", "High")
    
    st.subheader("Skill Penetration by Region")
    chart_data = pd.DataFrame(
        {"Region": ["North", "South", "East", "West"], "Skilled %": [45, 60, 30, 55]}
    )
    st.bar_chart(chart_data.set_index("Region"))
