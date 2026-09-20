"""
Step 2 — Extraction (LLM pass).
Sends each Utterance to the Gemini API and gets back a structured list
of candidate commitments in JSON.

Step 3 — Resolution.
Converts relative date phrases ("tomorrow", "Wednesday evening") into
absolute ISO-8601 datetimes, anchored to each utterance's own timestamp.
"""

import json
import os
import re
import time
from datetime import datetime, timedelta

from google import genai
from google.genai import types
from dateutil import parser as dateutil_parser

# ---------------------------------------------------------------------------
# Gemini client
# ---------------------------------------------------------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

MODEL_NAME = "gemini-3.6-flash"

# ---------------------------------------------------------------------------
# Extraction prompt
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are an executive assistant AI. Your job is to extract commitments and pending actions from business communications on behalf of Arjun Malhotra (VP Sales).

CRITICAL RULES:
1. Extract ONLY commitments that are relevant to Arjun — things Arjun owes someone, things others owe Arjun, or unresolved ownership questions that affect Arjun.
2. For each commitment, set "direction":
   - "arjun_owes" — Arjun has committed to doing something for someone else.
   - "arjun_waiting_on" — Someone else has committed to doing something for Arjun.
   - "fyi" — General awareness item, no direct action.
3. VOICE NOTE RULE: Voice notes are personal reminders dictated by Arjun to himself. Treat all statements in them as Arjun's own commitments or open items — NOT as instructions from a third party. For example, "expense report needs to be in my hands by Wednesday evening" in a voice note is Arjun RESTATING his own deadline (direction: arjun_waiting_on), not a new ask from Divya.
4. If ownership of a task is unclear, explicitly disputed, or disclaimed by multiple parties, set "ambiguous_owner": true. DO NOT guess who owns it.
5. For deadlines: capture the VERBATIM phrase from the text as "deadline_stated". Do NOT resolve it to a date — leave that to the resolution step.
6. Set "confidence": "high" if the commitment is explicit and unambiguous, "medium" if inferred, "low" if uncertain.
7. If a later message in a thread indicates a task is COMPLETED (e.g. "report attached", "confirmed, see you at 3"), set "completion_signal": true.

Return ONLY a valid JSON array. Each element must have exactly these fields:
{
  "action": "short description of what needs to be done",
  "topic_key": "snake_case keyword identifying the commitment (e.g. vendor_list, campaign_deck, meridian_call)",
  "direction": "arjun_owes" | "arjun_waiting_on" | "fyi",
  "responsible_party": "name of person who must act",
  "counterparty": "name of person the action is for / owed to",
  "deadline_stated": "verbatim deadline phrase from the text, or null",
  "ambiguous_owner": true | false,
  "completion_signal": true | false,
  "confidence": "high" | "medium" | "low",
  "evidence_source": "the source_id of this utterance"
}

Do not invent information. If a field is not determinable, use null."""


def _build_user_prompt(utterance: dict) -> str:
    channel = utterance["channel"]
    ts = utterance["timestamp"]
    speaker = utterance["speaker"]
    text = utterance["text"]

    context = f"Source type: {channel}\nTimestamp: {ts}\nSpeaker: {speaker}\n"
    if channel == "voice_note":
        context += "⚠️ This is a VOICE NOTE — a personal reminder from Arjun to himself. Apply the voice note rule.\n"
    if channel == "email":
        context += f"Thread subject: {utterance.get('thread_subject', '')}\n"
        context += f"Is Arjun the sender: {utterance.get('is_arjun', False)}\n"

    context += f"\nText:\n{text}"
    return context


def extract_candidates_llm(utterance: dict) -> list[dict]:
    """Call Gemini to extract candidate commitments from a single utterance."""
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY not set. Enter it in the sidebar and click Rebuild Ledger.")

    client = genai.Client(api_key=api_key)
    user_prompt = _build_user_prompt(utterance)

    max_retries = 3
    base_delay = 10
    
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.1,
                    response_mime_type="application/json",
                ),
            )
            break
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                if attempt < max_retries - 1:
                    print(f"  [Rate limit hit] Retrying in {base_delay}s...")
                    time.sleep(base_delay)
                    base_delay *= 2
                    continue
            raise

    raw = response.text.strip()
    # Strip markdown code fences if the model wraps the JSON
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    try:
        candidates = json.loads(raw)
        if isinstance(candidates, dict):
            candidates = next(iter(candidates.values()))
        for c in candidates:
            c.setdefault("evidence_source", utterance["source_id"])
        return candidates
    except json.JSONDecodeError as e:
        print(f"  ⚠ JSON parse error for {utterance['source_id']}: {e}")
        print(f"  Raw response: {raw[:300]}")
        return []


# ---------------------------------------------------------------------------
# Date resolution (deterministic)
# ---------------------------------------------------------------------------
WEEK_DAYS = {
    "monday": 0, "tuesday": 1, "wednesday": 2,
    "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6,
}

TIME_OF_DAY = {
    "morning": "09:00", "eod": "18:00", "end of day": "18:00",
    "evening": "18:00", "afternoon": "14:00", "noon": "12:00",
    "night": "20:00", "first thing": "09:00",
}


def resolve_deadline(stated: str | None, anchor_ts: str) -> str | None:
    """
    Convert a relative deadline phrase to an absolute ISO-8601 datetime string.
    anchor_ts: ISO-8601 timestamp of the message containing this deadline.
    Returns None if stated is None or unresolvable.
    """
    if not stated:
        return None

    anchor = datetime.fromisoformat(anchor_ts)
    s = stated.lower().strip()

    # Extract time-of-day hint
    time_str = "09:00"  # default
    for phrase, t in TIME_OF_DAY.items():
        if phrase in s:
            time_str = t
            break
    hour, minute = map(int, time_str.split(":"))

    # "today"
    if "today" in s:
        return anchor.replace(hour=hour, minute=minute, second=0, microsecond=0).isoformat()

    # "tomorrow"
    if "tomorrow" in s:
        d = (anchor + timedelta(days=1)).replace(hour=hour, minute=minute, second=0, microsecond=0)
        return d.isoformat()

    # Named day of week (e.g. "Wednesday", "Thursday morning")
    for day_name, day_num in WEEK_DAYS.items():
        if day_name in s:
            days_ahead = (day_num - anchor.weekday()) % 7
            if days_ahead == 0:
                days_ahead = 7  # next occurrence
            # If the text also mentions "this" or the day is within same week, use closest
            if f"this {day_name}" in s or days_ahead == 0:
                days_ahead = 0
            d = (anchor + timedelta(days=days_ahead)).replace(
                hour=hour, minute=minute, second=0, microsecond=0
            )
            return d.isoformat()

    # Specific time like "9:30 AM Thursday" — already covered above via day_name loop
    # Try dateutil as fallback for explicit date strings
    try:
        parsed = dateutil_parser.parse(stated, default=anchor)
        return parsed.replace(second=0, microsecond=0).isoformat()
    except Exception:
        return None


def extract_and_resolve_all(utterances: list[dict]) -> list[dict]:
    """
    Run extraction + resolution on every utterance.
    Returns a flat list of candidate commitment dicts, each with:
      - all fields from extract_candidates_llm
      - deadline_resolved: absolute ISO datetime or None
    """
    all_candidates = []
    for i, utt in enumerate(utterances):
        print(f"  [{i+1}/{len(utterances)}] Extracting from {utt['source_id']} ...")
        candidates = extract_candidates_llm(utt)
        for c in candidates:
            c["deadline_resolved"] = resolve_deadline(
                c.get("deadline_stated"), utt["timestamp"]
            )
            c["utterance_timestamp"] = utt["timestamp"]
        all_candidates.extend(candidates)
        print(f"    → {len(candidates)} candidate(s) found")

    print(f"\nTotal raw candidates: {len(all_candidates)}")
    return all_candidates


if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from pipeline.ingest import ingest_all

    data = ingest_all()
    candidates = extract_and_resolve_all(data["utterances"])
    print(json.dumps(candidates[:3], indent=2))
