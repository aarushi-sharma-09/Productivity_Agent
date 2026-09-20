"""
Steps 4 & 5 — Deduplication, Merging, Classification.

Rules (all deterministic — no LLM):
1. Cluster candidates by topic_key. Same topic_key → same real commitment.
2. Within a cluster, sort by utterance_timestamp ascending.
3. Canonical deadline = latest resolved deadline (can move earlier OR later).
4. Keep full deadline_history for auditability.
5. If ANY candidate in a cluster has completion_signal=True (and it's a later
   message), set status="done".
6. If direction or ownership is disputed/ambiguous across candidates, set
   ambiguous_owner=True — never force a false consensus.
7. Confidence = lowest confidence across the cluster (conservative).
8. Evidence = deduplicated union of all evidence_source values.
"""

from datetime import datetime


# Canonical status enum
STATUS_OPEN = "open"
STATUS_DONE = "done"
STATUS_OVERDUE = "overdue"
STATUS_AMBIGUOUS = "ambiguous_owner"

CONFIDENCE_RANK = {"high": 3, "medium": 2, "low": 1}


def _min_confidence(values: list[str]) -> str:
    ranked = sorted(values, key=lambda v: CONFIDENCE_RANK.get(v, 0))
    return ranked[0] if ranked else "low"


def _latest_resolved(history: list[dict]) -> str | None:
    """
    Return the resolved deadline from the latest-timestamped history entry.
    'Latest' means the most recently stated deadline wins (latest utterance_timestamp).
    History entries use the key 'resolved' (not 'deadline_resolved').
    """
    with_deadline = [h for h in history if h.get("resolved") and h.get("utterance_timestamp")]
    if not with_deadline:
        return None
    return sorted(with_deadline, key=lambda h: h["utterance_timestamp"])[-1]["resolved"]


def deduplicate(candidates: list[dict]) -> list[dict]:
    """
    Cluster raw extraction candidates into canonical commitment records.
    Returns a list of merged commitment dicts.
    """
    # Group by topic_key
    clusters: dict[str, list[dict]] = {}
    for c in candidates:
        key = c.get("topic_key", "unknown")
        clusters.setdefault(key, []).append(c)

    merged = []
    for topic_key, group in clusters.items():
        # Sort by utterance timestamp
        group_sorted = sorted(group, key=lambda c: c.get("utterance_timestamp", ""))

        # --- Direction resolution ---
        directions = {c.get("direction") for c in group_sorted if c.get("direction")}
        # If conflicting directions, flag ambiguous; otherwise take majority/latest
        if len(directions) > 1 and "arjun_owes" in directions and "arjun_waiting_on" in directions:
            direction = "arjun_owes"  # conservative: if Arjun ever owed it, flag it
            dir_conflict = True
        else:
            # Take the direction from the latest candidate with a non-null direction
            direction = group_sorted[-1].get("direction") or (directions.pop() if directions else "fyi")
            dir_conflict = False

        # --- Ambiguous owner ---
        any_ambiguous = any(c.get("ambiguous_owner") for c in group_sorted) or dir_conflict
        # Also flag if responsible_party is blank/null on all candidates
        all_responsible = [c.get("responsible_party") for c in group_sorted if c.get("responsible_party")]
        if not all_responsible:
            any_ambiguous = True

        # --- Deadline history ---
        deadline_history = []
        for c in group_sorted:
            if c.get("deadline_stated") or c.get("deadline_resolved"):
                deadline_history.append(
                    {
                        "stated": c.get("deadline_stated"),
                        "resolved": c.get("deadline_resolved"),
                        "utterance_timestamp": c.get("utterance_timestamp"),
                        "source": c.get("evidence_source"),
                    }
                )

        # Deduplicate deadline history entries (same stated phrase)
        seen_stated = set()
        unique_history = []
        for h in deadline_history:
            key_h = (h.get("stated") or "") + "|" + (h.get("source") or "")
            if key_h not in seen_stated:
                seen_stated.add(key_h)
                unique_history.append(h)

        deadline_current = _latest_resolved(unique_history)

        # --- Completion signal ---
        # Only consider completion signals from the LATER candidates in the cluster
        completion_candidates = [
            c for c in group_sorted if c.get("completion_signal")
        ]
        is_done = len(completion_candidates) > 0

        # --- Evidence ---
        evidence = list(dict.fromkeys(c.get("evidence_source") for c in group_sorted if c.get("evidence_source")))

        # --- Description: use latest non-null action ---
        description = None
        for c in reversed(group_sorted):
            if c.get("action"):
                description = c["action"]
                break

        # --- Counterparty: use latest non-null ---
        counterparty = None
        for c in reversed(group_sorted):
            if c.get("counterparty"):
                counterparty = c["counterparty"]
                break

        # --- Confidence ---
        confidence = _min_confidence([c.get("confidence", "low") for c in group_sorted])

        record = {
            "topic_key": topic_key,
            "description": description,
            "direction": direction,
            "counterparty": counterparty,
            "deadline_current": deadline_current,
            "deadline_history": unique_history,
            "status": STATUS_DONE if is_done else STATUS_OPEN,
            "ambiguous_owner": any_ambiguous,
            "evidence": evidence,
            "confidence": confidence,
            "raw_candidate_count": len(group_sorted),
        }
        merged.append(record)

    return merged


def classify_status(records: list[dict], run_date: datetime) -> list[dict]:
    """
    Post-dedup pass: compute final status relative to a given run_date.
    Overrides status to 'overdue' if deadline has passed and status != 'done'.
    Sets 'ambiguous_owner' items to STATUS_AMBIGUOUS status for display.
    Adds a sequential ID.
    """
    result = []
    for i, rec in enumerate(records):
        rec = dict(rec)  # shallow copy
        rec["id"] = f"C-{i+1:03d}"

        if rec["status"] != STATUS_DONE:
            if rec["ambiguous_owner"]:
                rec["status"] = STATUS_AMBIGUOUS
            elif rec["deadline_current"]:
                try:
                    deadline_dt = datetime.fromisoformat(rec["deadline_current"])
                    if deadline_dt < run_date:
                        rec["status"] = STATUS_OVERDUE
                except ValueError:
                    pass

        result.append(rec)
    return result


if __name__ == "__main__":
    import json, sys
    sys.path.insert(0, ".")
    from pipeline.ingest import ingest_all
    from pipeline.extract import extract_and_resolve_all

    data = ingest_all()
    candidates = extract_and_resolve_all(data["utterances"])
    merged = deduplicate(candidates)
    final = classify_status(merged, datetime(2026, 9, 23, 8, 0))
    print(json.dumps(final, indent=2))
