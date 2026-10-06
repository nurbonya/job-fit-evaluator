"""
Unit tests for database and prompt formatting.
"""

import os
import sqlite3
import pandas as pd
import pytest

from core.database import init_db, load_jobs_df, save_job_record
from core.prompts import build_evaluation_user_prompt

TEST_DB = "test_jobs.db"


@pytest.fixture(autouse=True)
def run_around_tests():
    """Setup and teardown temporary test SQLite database."""
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    init_db(db_file=TEST_DB)
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_prompt_generation():
    prompt = build_evaluation_user_prompt(
        resume_text="SQL and Tableau experience",
        job_title="Data Analyst",
        company="Acme Corp",
        job_description="Looking for SQL mastery.",
    )
    assert "Acme Corp" in prompt
    assert "SQL and Tableau experience" in prompt
    assert "Looking for SQL mastery." in prompt


def test_database_insert_and_load():
    job_id = save_job_record(
        company="Test Co",
        job_title="Senior Analyst",
        fit_score=85,
        step_up="Strong Step-Up",
        job_url="https://example.com/job",
        db_file=TEST_DB,
    )
    assert job_id == 1

    df = load_jobs_df(db_file=TEST_DB)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.iloc[0]["company"] == "Test Co"
    assert df.iloc[0]["fit_score"] == 85
