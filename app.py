"""
Job Strategy & Qualification Evaluator
A Streamlit web interface for evaluating job descriptions against verified candidate experience.
"""

from datetime import datetime
import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st

from core.database import init_db, load_jobs_df, save_job_record
from core.evaluator import evaluate_job

# Load environment configuration
load_dotenv()

# Page Setup
st.set_page_config(
    page_title="Job Fit & Strategy Evaluator",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Ensure Database is ready
init_db()

# ---------------------------------------------------------
# Sidebar: Settings & Baseline Resume
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuration")

    api_key = st.text_input(
        "OpenAI API Key",
        value=os.getenv("OPENAI_API_KEY", ""),
        type="password",
        help="Reads from .env or your environment variables by default.",
    )

    model_choice = st.selectbox(
        "Model Selection",
        ["gpt-4o-mini", "gpt-4o"],
        index=0,
        help="gpt-4o-mini offers fast, low-cost extraction; gpt-4o provides deeper synthesis.",
    )

    st.divider()
    st.header("📄 Candidate Source of Truth")
    st.caption("All evaluations strictly adhere to this text as the sole source of verified truth.")

    default_resume = """Data Analyst (3 years of experience)
Technical Stack: SQL, Python, R, Tableau, Excel, Git, Relational Databases.
Key Experience:
- Developed complex multi-table SQL queries to extract, clean, and validate data across enterprise systems.
- Built interactive Tableau dashboards for executive leadership tracking KPIs and operational metrics.
- Conducted trend, anomaly, and root-cause analysis to support data-informed decision-making.
- Partnered with stakeholders across business units to gather reporting specifications.
- Led cross-functional process improvements and data quality assurance workflows.
- Completed ML image classification and predictive modeling projects.
"""
    resume_context = st.text_area(
        "Resume / Experience Profile",
        value=default_resume,
        height=320,
    )

# ---------------------------------------------------------
# Main View: Tabs
# ---------------------------------------------------------
st.title("🎯 Job Strategy & Qualification Evaluator")
st.caption("Evidence-backed alignment, gap identification, and pipeline tracking.")

tab_eval, tab_history = st.tabs(["🔍 Evaluate New Job", "📊 Saved Pipeline Tracker"])

with tab_eval:
    c1, c2, c3 = st.columns([2, 2, 2])
    with c1:
        target_company = st.text_input("Company Name", placeholder="e.g., Acquisio Data Systems")
    with c2:
        target_title = st.text_input("Target Job Title", placeholder="e.g., Senior Data Analyst")
    with c3:
        target_url = st.text_input("Job Posting URL (Optional)", placeholder="https://...")

    target_jd = st.text_area(
        "Job Description Text",
        placeholder="Paste the full job posting requirements and responsibilities here...",
        height=240,
    )

    if st.button("🚀 Run Rigorous Fit Analysis", type="primary", use_container_width=True):
        if not api_key:
            st.error("Please supply an OpenAI API key in the sidebar or via .env.")
        elif not target_jd.strip():
            st.warning("Please provide a job description to evaluate.")
        elif not resume_context.strip():
            st.warning("Please provide candidate experience in the sidebar.")
        else:
            with st.spinner("Analyzing requirements against verified career history..."):
                try:
                    result = evaluate_job(
                        api_key=api_key,
                        model_name=model_choice,
                        resume_text=resume_context,
                        job_title=target_title or "Target Role",
                        company=target_company or "Target Company",
                        job_description=target_jd,
                    )

                    # Persist record locally
                    save_job_record(
                        company=target_company or "Unknown",
                        job_title=target_title or "Untitled Role",
                        fit_score=result.get("fit_score", 0),
                        step_up=result.get("step_up_verdict", "N/A"),
                        job_url=target_url or "",
                    )

                    st.success("Evaluation complete and recorded in your local database!")
                    st.divider()

                    # Header Metrics
                    m1, m2, m3 = st.columns([1, 1, 2])
                    with m1:
                        st.metric("Fit Score", f"{result.get('fit_score', 0)} / 100")
                    with m2:
                        st.metric("Step-Up Assessment", result.get("step_up_verdict", "N/A"))
                    with m3:
                        st.info(f"**Verdict:** {result.get('summary_verdict', 'No summary provided.')}")

                    # Two-Column Categorized Output
                    col_left, col_right = st.columns(2)

                    with col_left:
                        st.subheader("✅ 1. Qualifications Clearly Met")
                        for item in result.get("clearly_met", []):
                            with st.expander(f"📌 {item.get('requirement', 'Requirement')}", expanded=True):
                                st.markdown(f"**Documented Evidence:** {item.get('candidate_evidence')}")

                        st.subheader("💡 2. Transferable Experience")
                        for item in result.get("transferable_experience", []):
                            with st.expander(f"🔄 {item.get('requirement', 'Requirement')}", expanded=False):
                                st.markdown(f"**Supporting Experience:** {item.get('transferable_skill')}")

                    with col_right:
                        st.subheader("⚠️ 3. Missing or Unverified Qualifications")
                        for item in result.get("missing_or_unverified", []):
                            with st.expander(f"🚫 {item.get('gap', 'Gap')}", expanded=True):
                                st.markdown(f"**Guidance:** {item.get('guidance')}")

                        st.subheader("❓ 4. Questions & Possible Dealbreakers")
                        for item in result.get("dealbreakers_and_questions", []):
                            with st.expander(f"🔍 {item.get('topic', 'Point of Inquiry')}", expanded=False):
                                st.markdown(f"**Interview Question:** *\"{item.get('question')}\"*")

                    st.divider()
                    st.subheader("🎯 Tailored Interview Highlights")
                    for pitch in result.get("tailored_pitch_points", []):
                        st.markdown(f"- {pitch}")

                except Exception as e:
                    st.error(f"Execution Error: {str(e)}")

with tab_history:
    st.subheader("📋 Tracked Opportunity Pipeline")
    jobs_df = load_jobs_df()
    if not jobs_df.empty:
        st.dataframe(
            jobs_df[
                [
                    "id",
                    "evaluated_at",
                    "company",
                    "job_title",
                    "fit_score",
                    "step_up_assessment",
                    "status",
                    "job_url",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )
        csv_bytes = jobs_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Export Pipeline to CSV",
            data=csv_bytes,
            file_name=f"job_tracker_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )
    else:
        st.info("No job evaluations recorded yet. Run your first analysis in the tab above!")
