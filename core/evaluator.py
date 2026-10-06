"""
Service layer communicating with the OpenAI LLM client.
"""

import json
from typing import Any, Dict
from openai import OpenAI
from core.prompts import SYSTEM_PROMPT, build_evaluation_user_prompt


def evaluate_job(
    api_key: str,
    model_name: str,
    resume_text: str,
    job_title: str,
    company: str,
    job_description: str,
) -> Dict[str, Any]:
    """Sends the resume and job posting to the LLM and returns the parsed 4-category JSON response."""
    client = OpenAI(api_key=api_key)
    prompt = build_evaluation_user_prompt(
        resume_text=resume_text,
        job_title=job_title,
        company=company,
        job_description=job_description,
    )

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )

    raw_content = response.choices[0].message.content
    return json.loads(raw_content)
