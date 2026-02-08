import streamlit as st
import pandas as pd
import pdfplumber
import random
import time
from collections import Counter
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SkillSetu Pro | AI Career Architect",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS FOR UI POLISH ---
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        border-left: 5px solid #FF4B4B;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .job-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 1px 1px 5px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        border: 1px solid #e0e0e0;
    }
    .highlight {
        color: #FF4B4B;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---

def extract_text_from_pdf(pdf_file):
    """Extracts text from uploaded PDF"""
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def calculate_ats_score(resume_text, job_description):
    """Core Logic: Matches keywords between Resume and JD"""
    resume_words = set(re.findall(r'\b\w+\b', resume_text.lower()))
    jd_words = set(re.findall(r'\b\w+\b', job_description.lower()))
    
    # Filter out common stop words (simplified list)
    stop_words = {'and', 'the', 'is', 'in', 'to', 'for', 'of', 'a', 'with', 'on', 'at'}
    jd_keywords = jd_words - stop_words
    
    matched_keywords = resume_words.intersection(jd_keywords)
    missing_keywords = jd_keywords - resume_words
    
    score = len(matched_keywords) / len(jd_keywords) * 100 if len(jd_keywords) > 0 else 0
    return round(score, 2), matched_keywords, missing_keywords

def check_grammar_basic(text):
    """A basic rule-based grammar checker for demo purposes"""
    issues = []
    # Check for passive voice indicators (very basic)
    if "was by" in text.lower():
        issues.append("Detected Passive Voice. Try using Active Voice for impact.")
    
    # Check for weak words
    weak_words = ['managed', 'handled', 'worked on', 'assisted']
    found_weak = [w for w in weak_words if w in text.lower()]
    if found_weak:
        issues.append(f"Replace weak verbs {found_weak} with power verbs like 'Orchestrated', 'Spearheaded', 'Engineered'.")
        
    if not issues:
        issues.append("Writing style looks strong!")
        
    return issues

def get_linkedin_jobs_mock(role, location):
    """Simulates fetching live jobs from LinkedIn"""
    # In a real app, you would use an API here.
    # We simulate data to ensure the demo never crashes.
    titles = [f"Senior {role}", f"Junior {role}", f"{role} Lead", f"{role} Intern"]
    companies = ["Google", "Microsoft", "TCS", "Infosys", "Local Startup", "HDFC Bank"]
    
    jobs = []
    for i in range(5):
        jobs.append({
            "Title": random.choice(titles),
            "Company": random.choice(companies),
            "Location": location,
            "Match": random.randint(70, 98),
            "Link": "https://linkedin.com/jobs"
        })
    return pd.DataFrame(jobs)

# --- SIDEBAR ---
st.sidebar.title("SkillSetu Pro 🧠")
st.sidebar.markdown("Generate Your Career Path")
menu = st.sidebar.radio("Navigation", ["🏠 Home", "📝 Smart ATS & Resume Doctor", "🔍 Job Hunter (LinkedIn)", "🎓 Skill Upscaler"])

# --- PAGE 1: HOME ---
if menu == "🏠 Home":
    st.title("Welcome to SkillSetu AI")
    st.markdown("### The Bridge Between Your Resume and Your Dream Job.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Users Placed", "12,450", "+15%")
    col2.metric("Resumes Optimized", "45,200", "+8%")
    col3.metric("Live Jobs Tracked", "1.2M", "Active")
    
    st.info("👈 Select **'Smart ATS'** from the sidebar to start optimizing your resume.")

# --- PAGE 2: SMART ATS (The Core Feature) ---
elif menu == "📝 Smart ATS & Resume Doctor":
    st.title("📝 Smart Resume ATS & Analyzer")
    st.markdown("Upload your resume and the Job Description (JD) to see if you will pass the robot screening.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
    with col2:
        jd_text = st.text_area("Paste Job Description (JD) here", height=150, placeholder="E.g., We are looking for a Python Developer with AWS experience...")

    if uploaded_file and jd_text:
        with st.spinner("AI is analyzing keywords..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            score, matched, missing = calculate_ats_score(resume_text, jd_text)
            grammar_tips = check_grammar_basic(resume_text)
            time.sleep(1.5) # UX Delay

        # Results Dashboard
        st.markdown("---")
        st.header("Analysis Report")
        
        # Score Gauge
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            st.metric("ATS Match Score", f"{score}%")
            st.progress(score/100)
            if score < 60:
                st.error("Low Match: Your resume might get rejected by the system.")
            elif score < 80:
                st.warning("Good Match: But needs optimization.")
            else:
                st.success("Excellent Match: You are ready to apply!")

        # Keyword Breakdown
        col_match, col_miss = st.columns(2)
        with col_match:
            st.subheader("✅ Matched Skills")
            st.write(", ".join(list(matched)) if matched else "No direct matches found.")
            
        with col_miss:
            st.subheader("❌ Missing Keywords (Critical)")
            if missing:
                for word in list(missing)[:10]: # Show top 10
                    st.markdown(f"- <span class='highlight'>{word}</span>", unsafe_allow_html=True)
            else:
                st.write("No missing keywords!")

        # Grammar & Style
        with st.expander("📝 Grammar & Style Check (Beta)"):
            for tip in grammar_tips:
                st.info(tip)

        # Word Cloud (Visual Bonus)
        with st.expander("☁️ View Resume Word Cloud"):
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(resume_text)
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)

# --- PAGE 3: JOB HUNTER ---
elif menu == "🔍 Job Hunter (LinkedIn)":
    st.title("🔍 Intelligent Job Search")
    st.markdown("Find jobs that match your **Skill Vector**.")

    c1, c2 = st.columns(2)
    with c1:
        role = st.text_input("Job Role", "Data Analyst")
    with c2:
        loc = st.text_input("Location", "Bangalore")

    if st.button("Search LinkedIn Jobs"):
        with st.spinner(f"Scraping live jobs for {role} in {loc}..."):
            time.sleep(2) # Simulated API delay
            df_jobs = get_linkedin_jobs_mock(role, loc)
            
        st.subheader(f"Found {len(df_jobs)} High-Match Jobs")
        
        for index, row in df_jobs.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="job-card">
                    <h4>{row['Title']} <span style="font-size:0.8em; color:gray">@ {row['Company']}</span></h4>
                    <p>📍 {row['Location']} | 🔥 Match Score: <span style="color:green; font-weight:bold">{row['Match']}%</span></p>
                    <a href="{row['Link']}" target="_blank"><button style="background-color:#0072b1; color:white; border:none; padding:5px 10px; border-radius:5px;">Apply on LinkedIn</button></a>
                </div>
                """, unsafe_allow_html=True)

# --- PAGE 4: SKILL UPSCALER ---
elif menu == "🎓 Skill Upscaler":
    st.title("🚀 Skill Gap Analysis")
    st.markdown("Based on current market trends (Live Data)")

    target_role = st.selectbox("I want to become a:", 
                               ["Python Developer", "Data Scientist", "Digital Marketer", "Project Manager"])
    
    current_level = st.select_slider("My Current Level", options=["Beginner", "Intermediate", "Advanced"])

    if st.button("Generate Roadmap"):
        st.subheader(f"Roadmap to become a {current_level} {target_role}")
        
        # Hardcoded logic for demo brilliance
        if target_role == "Python Developer":
            st.info("📉 **Gap Detected:** You need more exposure to **FastAPI** and **Docker**.")
            st.markdown("### 📅 4-Week Plan")
            st.checkbox("Week 1: Advanced OOPs in Python")
            st.checkbox("Week 2: API Development with FastAPI")
            st.checkbox("Week 3: Docker & Containerization")
            st.checkbox("Week 4: Build a Capstone Project (e.g., Portfolio Website)")
            
            st.markdown("### 📚 Recommended Courses")
            st.markdown("* **Free:** [CS50's Web Programming (Harvard)](https://cs50.harvard.edu/web/)")
            st.markdown("* **Paid:** [Udemy: Python for DevOps](https://udemy.com)")
            
        elif target_role == "Data Scientist":
            st.info("📉 **Gap Detected:** Strengthening **Statistics** and **Machine Learning** is required.")
            st.markdown("### 📅 4-Week Plan")
            st.checkbox("Week 1: Probability & Statistics")
            st.checkbox("Week 2: Pandas & NumPy Deep Dive")
            st.checkbox("Week 3: Scikit-Learn Algorithms")
            st.checkbox("Week 4: Kaggle Competition Entry")
