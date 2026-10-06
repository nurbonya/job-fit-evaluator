"""
SQLite database management for tracking evaluated applications.
"""

from datetime import datetime
import sqlite3
import pandas as pd

DEFAULT_DB_FILE = "job_applications.db"


def init_db(db_file: str = DEFAULT_DB_FILE) -> None:
    """Initializes the database table if it doesn't already exist."""
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            evaluated_at TEXT,
            company TEXT,
            job_title TEXT,
            fit_score INTEGER,
            step_up_assessment TEXT,
            status TEXT,
            job_url TEXT,
            notes TEXT
        )
    """
    )
    conn.commit()
    conn.close()


def save_job_record(
    company: str,
    job_title: str,
    fit_score: int,
    step_up: str,
    job_url: str = "",
    status: str = "Evaluating",
    notes: str = "",
    db_file: str = DEFAULT_DB_FILE,
) -> int:
    """Saves an evaluated job record and returns its inserted ID."""
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO jobs (evaluated_at, company, job_title, fit_score, step_up_assessment, status, job_url, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            company,
            job_title,
            fit_score,
            step_up,
            status,
            job_url,
            notes,
        ),
    )
    inserted_id = c.lastrowid
    conn.commit()
    conn.close()
    return inserted_id


def load_jobs_df(db_file: str = DEFAULT_DB_FILE) -> pd.DataFrame:
    """Reads all saved jobs into a pandas DataFrame ordered chronologically descending."""
    conn = sqlite3.connect(db_file)
    df = pd.read_sql_query("SELECT * FROM jobs ORDER BY id DESC", conn)
    conn.close()
    return df
