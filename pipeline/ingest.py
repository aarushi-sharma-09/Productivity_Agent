"""
Step 1 — Ingestion & Normalization.
Converts all raw sources into a uniform list of Utterance dicts.

Each Utterance:
{
    "source_id": str,
    "channel": "transcript" | "email" | "voice_note" | "calendar",
    "timestamp": ISO-8601 str,
    "speaker": str,          # name of the person who said/wrote it
    "is_arjun": bool,        # True if the speaker IS Arjun Malhotra
    "counterparties": list[str],  # other people involved in the message
    "text": str,
}
"""

from data.raw_sources import (
    TRANSCRIPT,
    EMAIL_THREADS,
    VOICE_NOTES,
    CALENDARS,
    PEOPLE,
    ARJUN_EMAIL,
)

ARJUN_NAME = "Arjun Malhotra"


def _resolve_name(email: str) -> str:
    return PEOPLE.get(email, email)


def ingest_transcript() -> list[dict]:
    """Wrap the full meeting transcript as a single Utterance."""
    return [
        {
            "source_id": TRANSCRIPT["source_id"],
            "channel": "transcript",
            "timestamp": TRANSCRIPT["timestamp"],
            "speaker": "Multiple (Arjun Malhotra, Neha Kapoor, Raghav Sethi, Divya Rao)",
            "is_arjun": True,  # Arjun is a key speaker; flag True to ensure his lines are extracted
            "counterparties": ["Neha Kapoor", "Raghav Sethi", "Divya Rao"],
            "text": TRANSCRIPT["text"],
        }
    ]


def ingest_emails() -> list[dict]:
    """Flatten all email threads into individual Utterances."""
    utterances = []
    for thread in EMAIL_THREADS:
        for email in thread["emails"]:
            sender_name = _resolve_name(email["from"])
            to_name = _resolve_name(email["to"])
            is_arjun = email["from"] == ARJUN_EMAIL
            counterparties = [to_name] if to_name != "All Staff" else []
            utterances.append(
                {
                    "source_id": email["source_id"],
                    "channel": "email",
                    "timestamp": email["timestamp"],
                    "speaker": sender_name,
                    "is_arjun": is_arjun,
                    "counterparties": counterparties,
                    "text": email["body"],
                    "thread_subject": thread["subject"],
                    "thread_id": thread["thread_id"],
                }
            )
    return utterances


def ingest_voice_notes() -> list[dict]:
    """Wrap voice notes as Arjun's own Utterances."""
    utterances = []
    for vn in VOICE_NOTES:
        utterances.append(
            {
                "source_id": vn["source_id"],
                "channel": "voice_note",
                "timestamp": vn["timestamp"],
                "speaker": vn["speaker"],
                "is_arjun": True,
                "counterparties": [],
                "text": vn["text"],
            }
        )
    return utterances


def ingest_calendars() -> list[dict]:
    """
    Calendars are used for context in the Daily Brief (not for commitment extraction).
    Return them as structured dicts, not Utterances.
    """
    events = []
    for person, entries in CALENDARS.items():
        for entry in entries:
            events.append(
                {
                    "person": person,
                    "date": entry["date"],
                    "time": entry["time"],
                    "event": entry["event"],
                }
            )
    return events


def ingest_all() -> dict:
    """
    Returns:
        {
            "utterances": list[Utterance],   # for LLM extraction
            "calendar_events": list[dict],   # for brief context
        }
    """
    utterances = (
        ingest_transcript()
        + ingest_emails()
        + ingest_voice_notes()
    )
    # Sort by timestamp so the extraction pass sees events in order
    utterances.sort(key=lambda u: u["timestamp"])
    return {
        "utterances": utterances,
        "calendar_events": ingest_calendars(),
    }


if __name__ == "__main__":
    import json
    result = ingest_all()
    print(f"Utterances: {len(result['utterances'])}")
    print(f"Calendar events: {len(result['calendar_events'])}")
    print(json.dumps(result["utterances"][0], indent=2))
