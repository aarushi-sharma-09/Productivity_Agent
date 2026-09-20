"""
Pytest tests for the deduplication engine.
Tests the two critical invariants:
  1. Latest-timestamp-wins for conflicting deadlines.
  2. A done-signal from a later email overrides an earlier open state.
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.dedup import deduplicate, classify_status, STATUS_DONE, STATUS_OVERDUE, STATUS_OPEN, STATUS_AMBIGUOUS


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_candidate(
    topic_key: str,
    action: str,
    direction: str = "arjun_owes",
    counterparty: str = "Raghav Sethi",
    responsible_party: str = "Arjun Malhotra",
    deadline_stated: str | None = None,
    deadline_resolved: str | None = None,
    utterance_timestamp: str = "2026-09-21T09:00:00",
    completion_signal: bool = False,
    ambiguous_owner: bool = False,
    confidence: str = "high",
    evidence_source: str = "transcript#1",
) -> dict:
    return {
        "topic_key": topic_key,
        "action": action,
        "direction": direction,
        "counterparty": counterparty,
        "responsible_party": responsible_party,
        "deadline_stated": deadline_stated,
        "deadline_resolved": deadline_resolved,
        "utterance_timestamp": utterance_timestamp,
        "completion_signal": completion_signal,
        "ambiguous_owner": ambiguous_owner,
        "confidence": confidence,
        "evidence_source": evidence_source,
    }


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestDedup:

    def test_single_candidate_passes_through(self):
        candidates = [make_candidate("vendor_list", "Send vendor list to Raghav")]
        result = deduplicate(candidates)
        assert len(result) == 1
        assert result[0]["topic_key"] == "vendor_list"

    def test_multiple_candidates_same_topic_collapsed(self):
        candidates = [
            make_candidate("vendor_list", "Send vendor list", utterance_timestamp="2026-09-21T09:00:00", evidence_source="transcript#1"),
            make_candidate("vendor_list", "Send vendor list today", utterance_timestamp="2026-09-21T09:50:00", evidence_source="email#T1-1"),
            make_candidate("vendor_list", "Send vendor list tomorrow", utterance_timestamp="2026-09-21T17:40:00", evidence_source="email#T1-2"),
        ]
        result = deduplicate(candidates)
        assert len(result) == 1
        assert result[0]["raw_candidate_count"] == 3

    def test_latest_timestamp_wins_for_deadline(self):
        """The most recently stated deadline should be the canonical one."""
        candidates = [
            make_candidate(
                "vendor_list", "Send today",
                deadline_stated="today", deadline_resolved="2026-09-21T18:00:00",
                utterance_timestamp="2026-09-21T09:00:00",
            ),
            make_candidate(
                "vendor_list", "Send tomorrow morning",
                deadline_stated="tomorrow morning", deadline_resolved="2026-09-22T09:00:00",
                utterance_timestamp="2026-09-21T17:40:00",
            ),
            make_candidate(
                "vendor_list", "Send Wednesday morning",
                deadline_stated="tomorrow (Wednesday) morning", deadline_resolved="2026-09-23T09:00:00",
                utterance_timestamp="2026-09-22T18:30:00",
            ),
        ]
        result = deduplicate(candidates)
        assert len(result) == 1
        # Latest utterance timestamp → Wednesday deadline
        assert result[0]["deadline_current"] == "2026-09-23T09:00:00"

    def test_deadline_can_move_earlier(self):
        """Deadlines can move to an earlier date (expense report: Thu → Wed)."""
        candidates = [
            make_candidate(
                "expense_report", "Deliver expense report by Thursday",
                deadline_stated="Thursday morning", deadline_resolved="2026-09-24T09:00:00",
                utterance_timestamp="2026-09-21T14:30:00",
                direction="arjun_waiting_on",
            ),
            make_candidate(
                "expense_report", "Deliver expense report by Wednesday evening",
                deadline_stated="Wednesday evening", deadline_resolved="2026-09-23T18:00:00",
                utterance_timestamp="2026-09-22T09:00:00",
                direction="arjun_waiting_on",
            ),
        ]
        result = deduplicate(candidates)
        # Latest utterance says Wednesday → that's canonical even though it's earlier
        assert result[0]["deadline_current"] == "2026-09-23T18:00:00"

    def test_done_signal_overrides_open(self):
        """A completion signal from a later message marks the commitment as done."""
        candidates = [
            make_candidate(
                "meridian_call", "Confirm call with Priya",
                utterance_timestamp="2026-09-21T13:00:00",
                completion_signal=False,
            ),
            make_candidate(
                "meridian_call", "Call confirmed for 3PM",
                utterance_timestamp="2026-09-22T17:45:00",
                completion_signal=True,
            ),
        ]
        result = deduplicate(candidates)
        assert result[0]["status"] == STATUS_DONE

    def test_ambiguous_owner_propagates(self):
        """If any candidate flags ambiguous_owner, the merged record must too."""
        candidates = [
            make_candidate("mumbai_lease", "Mumbai lease sign-off", ambiguous_owner=False),
            make_candidate("mumbai_lease", "Mumbai lease — no owner confirmed", ambiguous_owner=True),
        ]
        result = deduplicate(candidates)
        assert result[0]["ambiguous_owner"] is True

    def test_evidence_union(self):
        """Evidence sources from all candidates are merged (deduped)."""
        candidates = [
            make_candidate("vendor_list", "Send vendor list", evidence_source="transcript#1"),
            make_candidate("vendor_list", "Send vendor list", evidence_source="email#T1-1"),
            make_candidate("vendor_list", "Send vendor list", evidence_source="email#T1-2"),
        ]
        result = deduplicate(candidates)
        evidence = result[0]["evidence"]
        assert "transcript#1" in evidence
        assert "email#T1-1" in evidence
        assert "email#T1-2" in evidence
        assert len(evidence) == 3

    def test_confidence_is_minimum(self):
        """Confidence should be the lowest across all candidates (conservative)."""
        candidates = [
            make_candidate("vendor_list", "Send vendor list", confidence="high"),
            make_candidate("vendor_list", "Maybe send vendor list", confidence="low"),
        ]
        result = deduplicate(candidates)
        assert result[0]["confidence"] == "low"

    def test_different_topics_not_merged(self):
        """Commitments with different topic keys must remain separate."""
        candidates = [
            make_candidate("vendor_list", "Send vendor list"),
            make_candidate("campaign_deck", "Review campaign deck"),
            make_candidate("mumbai_lease", "Mumbai lease sign-off"),
        ]
        result = deduplicate(candidates)
        assert len(result) == 3

    def test_classify_status_open(self):
        run_date = datetime(2026, 9, 22, 8, 0)
        records = [{"topic_key": "t", "description": "x", "direction": "arjun_owes",
                    "deadline_current": "2026-09-23T09:00:00", "status": STATUS_OPEN,
                    "ambiguous_owner": False, "evidence": [], "confidence": "high",
                    "deadline_history": [], "counterparty": "X", "raw_candidate_count": 1}]
        result = classify_status(records, run_date)
        assert result[0]["status"] == STATUS_OPEN

    def test_classify_status_overdue(self):
        run_date = datetime(2026, 9, 24, 8, 0)
        records = [{"topic_key": "t", "description": "x", "direction": "arjun_owes",
                    "deadline_current": "2026-09-23T09:00:00", "status": STATUS_OPEN,
                    "ambiguous_owner": False, "evidence": [], "confidence": "high",
                    "deadline_history": [], "counterparty": "X", "raw_candidate_count": 1}]
        result = classify_status(records, run_date)
        assert result[0]["status"] == STATUS_OVERDUE

    def test_classify_done_not_overridden_to_overdue(self):
        """A done task must never be reclassified as overdue, even if deadline passed."""
        run_date = datetime(2026, 9, 25, 8, 0)
        records = [{"topic_key": "t", "description": "x", "direction": "arjun_owes",
                    "deadline_current": "2026-09-22T09:00:00", "status": STATUS_DONE,
                    "ambiguous_owner": False, "evidence": [], "confidence": "high",
                    "deadline_history": [], "counterparty": "X", "raw_candidate_count": 1}]
        result = classify_status(records, run_date)
        assert result[0]["status"] == STATUS_DONE

    def test_classify_ambiguous_sets_status(self):
        run_date = datetime(2026, 9, 23, 8, 0)
        records = [{"topic_key": "t", "description": "x", "direction": "fyi",
                    "deadline_current": "2026-09-25T18:00:00", "status": STATUS_OPEN,
                    "ambiguous_owner": True, "evidence": [], "confidence": "medium",
                    "deadline_history": [], "counterparty": "Facilities", "raw_candidate_count": 2}]
        result = classify_status(records, run_date)
        assert result[0]["status"] == STATUS_AMBIGUOUS

    def test_ids_assigned(self):
        records = [
            {"topic_key": "a", "description": "x", "direction": "arjun_owes",
             "deadline_current": None, "status": STATUS_OPEN, "ambiguous_owner": False,
             "evidence": [], "confidence": "high", "deadline_history": [], "counterparty": "X", "raw_candidate_count": 1},
            {"topic_key": "b", "description": "y", "direction": "arjun_owes",
             "deadline_current": None, "status": STATUS_OPEN, "ambiguous_owner": False,
             "evidence": [], "confidence": "high", "deadline_history": [], "counterparty": "Y", "raw_candidate_count": 1},
        ]
        result = classify_status(records, datetime(2026, 9, 21, 8, 0))
        assert result[0]["id"] == "C-001"
        assert result[1]["id"] == "C-002"
