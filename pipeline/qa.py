"""
Step 7b — Q&A Interface.
Reads the ledger (never rewrites it) and uses Gemini to phrase answers
to natural-language questions about Arjun's commitments.
"""

import json
import os
import re
from datetime import datetime

from google import genai
from google.genai import types

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

MODEL_NAME = "gemini-3.6-flash"

QA_SYSTEM_PROMPT = """You are a precise executive assistant AI for Arjun Malhotra (VP Sales).
You have access to a structured commitment ledger derived from Arjun's meetings, emails, and voice notes.

Your job: answer Arjun's questions about his commitments accurately and concisely.

STRICT RULES:
1. Answer ONLY based on the ledger data provided. Do not invent or infer facts not present in the ledger.
2. If the ledger shows a task has ambiguous ownership, say so explicitly — do not guess the owner.
3. When relevant, mention the status (open, overdue, done), the deadline, and who else is involved.
4. Cite the evidence sources (e.g., email#T1-4, voicenote#1) when they strengthen the answer.
5. Be concise — this is a quick-reference brief, not a report. Use bullet points for multiple items.
6. If the question cannot be answered from the ledger data, say so clearly."""


def answer_question(question: str, ledger: dict) -> str:
    """
    Answer a natural-language question about Arjun's commitments.
    Uses the full ledger as context but reads it as JSON (no regeneration).
    """
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return "⚠️ GEMINI_API_KEY not set. Enter it in the sidebar first."

    commitments = ledger.get("commitments", [])
    calendar = ledger.get("calendar_events", [])
    arjun_calendar = [e for e in calendar if e["person"] == "Arjun Malhotra"]

    ledger_context = json.dumps(
        {"commitments": commitments, "arjun_calendar": arjun_calendar},
        indent=2,
    )

    user_prompt = f"""Here is the commitment ledger for Arjun Malhotra:

<ledger>
{ledger_context}
</ledger>

Question from Arjun: {question}

Answer:"""

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=QA_SYSTEM_PROMPT,
            temperature=0.2,
        ),
    )
    return response.text.strip()


def answer_what_needs_action_today(run_date: datetime, ledger: dict) -> str:
    """
    Specialised handler for "What needs action today?" queries.
    Filters the ledger first, then asks the LLM to phrase the answer.
    This is the most important query to get right.
    """
    from pipeline.ledger import get_commitments_for_date

    brief = get_commitments_for_date(run_date)

    # Build a focused context for this specific question
    focus = {
        "run_date": run_date.strftime("%A %d %B %Y"),
        "my_actions_due_today": brief["my_actions"],
        "overdue_items": brief["overdue"],
        "ambiguous_ownership": brief["ambiguous"],
        "calendar_today": brief["calendar_today"],
    }

    question = f"What needs action today ({run_date.strftime('%A %d %B')}), and is anything overdue or stuck?"
    return answer_question(question, {"commitments": ledger["commitments"], "focus": focus})


if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from pipeline.ledger import load_ledger

    ledger = load_ledger(run_date=datetime(2026, 9, 23, 8, 0))

    questions = [
        "What did I promise Raghav?",
        "What needs action today?",
        "Who is handling the Mumbai lease?",
        "Is the expense report done?",
    ]
    for q in questions:
        print(f"\nQ: {q}")
        print(f"A: {answer_question(q, ledger)}")
        print("-" * 60)
