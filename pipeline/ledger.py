"""
Step 6 — Ledger management.
Runs the full pipeline (ingest → extract → dedup → classify) and writes
the result to ledger.json. Also provides read functions for the frontend.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Ensure repo root is on path when run directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.ingest import ingest_all
from pipeline.extract import extract_and_resolve_all
from pipeline.dedup import deduplicate, classify_status

LEDGER_PATH = Path(__file__).parent.parent / "ledger.json"


def build_ledger(run_date: datetime | None = None, force_rebuild: bool = False) -> dict:
    """
    Build (or reload) the commitment ledger.

    Args:
        run_date:      Date/time to use for overdue classification.
                       Defaults to now if not provided.
        force_rebuild: If True, always re-run the full LLM extraction pipeline.
                       If False (default), load from ledger.json if it exists.

    Returns:
        A dict with keys "commitments" and "calendar_events".
    """
    if not force_rebuild and LEDGER_PATH.exists():
        with open(LEDGER_PATH) as f:
            ledger = json.load(f)
        # Re-classify status against the requested run_date
        if run_date:
            ledger["commitments"] = classify_status(ledger["commitments"], run_date)
        return ledger

    print("🔄 Running full pipeline (extract + dedup)...")
    data = ingest_all()
    print(f"  Ingested {len(data['utterances'])} utterances.")

    candidates = extract_and_resolve_all(data["utterances"])

    merged = deduplicate(candidates)
    if run_date is None:
        run_date = datetime.now()
    final_commitments = classify_status(merged, run_date)

    ledger = {
        "generated_at": datetime.now().isoformat(),
        "commitments": final_commitments,
        "calendar_events": data["calendar_events"],
    }

    with open(LEDGER_PATH, "w") as f:
        json.dump(ledger, f, indent=2)

    print(f"✅ Ledger written to {LEDGER_PATH}")
    print(f"   {len(final_commitments)} canonical commitments.")
    return ledger


def load_ledger(run_date: datetime | None = None) -> dict:
    """Load ledger.json, re-classifying status for the given run_date."""
    if not LEDGER_PATH.exists():
        raise FileNotFoundError(
            "ledger.json not found. Run `python pipeline/ledger.py` or click 'Rebuild Ledger' in the app."
        )
    with open(LEDGER_PATH) as f:
        ledger = json.load(f)

    if run_date:
        # Re-run status classification on the stored commitments
        ledger["commitments"] = classify_status(ledger["commitments"], run_date)
    return ledger


def get_commitments_for_date(run_date: datetime) -> dict:
    """
    Return commitments partitioned by status for a given run_date.
    Used by the Daily Brief view.
    """
    ledger = load_ledger(run_date=run_date)
    commitments = ledger["commitments"]

    # Calendar events for just this date
    date_str = run_date.strftime("%Y-%m-%d")
    calendar_today = [
        e for e in ledger["calendar_events"]
        if e["person"] == "Arjun Malhotra" and e["date"] == date_str
    ]

    return {
        "run_date": run_date.isoformat(),
        "my_actions": [c for c in commitments if c["direction"] == "arjun_owes" and c["status"] not in ("done", "overdue", "ambiguous_owner")],
        "overdue": [c for c in commitments if c["status"] == "overdue"],
        "waiting_on": [c for c in commitments if c["direction"] == "arjun_waiting_on" and c["status"] != "done"],
        "ambiguous": [c for c in commitments if c["status"] == "ambiguous_owner"],
        "done": [c for c in commitments if c["status"] == "done"],
        "calendar_today": sorted(calendar_today, key=lambda e: e["time"]),
    }


if __name__ == "__main__":
    # Default run: Wed 23 Sep 08:00 (the critical test date)
    run_dt = datetime(2026, 9, 23, 8, 0)
    ledger = build_ledger(run_date=run_dt, force_rebuild=True)
    brief = get_commitments_for_date(run_dt)
    print("\n=== DAILY BRIEF — Wed 23 Sep ===")
    for section, items in brief.items():
        if section in ("run_date",):
            continue
        print(f"\n[{section.upper()}]")
        if isinstance(items, list):
            for item in items:
                print(f"  • {item.get('description', item.get('event', '?'))}")
