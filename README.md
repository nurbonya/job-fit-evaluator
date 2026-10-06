# job-fit-evaluator
An AI-powered job evaluation and application tracker designed for professionals leveling up into higher-paying, advanced roles. 
# 🎯 Job Fit & Strategy Evaluator

An AI-powered job evaluation and application tracker designed for professionals leveling up into higher-paying, advanced roles. 

Unlike generic resume tools that indiscriminately rewrite bullet points with keywords, this application acts as an **objective auditor**. It treats your uploaded resume as the absolute single source of truth, performs strict gap analysis, and generates strategic interview questions.

---

## ✨ Features

- **Strict Source-of-Truth Enforcement:** Never invents or assumes qualifications that aren't explicitly verified in your profile.
- **4-Category Objective Audit:**
  - ✅ **Qualifications Clearly Met:** Grounded directly in your past metrics and roles.
  - 💡 **Transferable Experience:** Identifies adjacent technical projects and skills.
  - ⚠️ **Missing or Unverified:** Flags genuine gaps without hallucinating.
  - ❓ **Dealbreakers & Questions to Investigate:** Formulates tactical questions regarding team seniority, tech stack maturity, and on-call expectations.
- **Embedded Pipeline Tracker:** Automatically saves evaluations to a local SQLite database (`job_applications.db`) with one-click CSV export.
- **Privacy First:** Runs locally on your machine with your own API key.

---

## 🚀 Quickstart

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/job-fit-evaluator.git
cd job-fit-evaluator
