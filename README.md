# ⚡ ExecBrief — Executive Productivity Agent

> **Assignment 1 · AIONOS Agentic AI Factory**

An AI agent that turns Arjun Malhotra's scattered executive inputs (meeting transcripts, calendars, emails, voice notes) into a clean, deduplicated Daily Action Brief with a Q&A interface.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Streamlit](https://img.shields.io/badge/UI-Streamlit-red) ![LLM](https://img.shields.io/badge/LLM-Gemini%202.0%20Flash-yellow)

---

## Live Demo

> **[Streamlit Community Cloud link — add after deployment]**

---

## One-Command Local Run

```bash
git clone <repo-url>
cd Aionos_Assignemnt

python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

export GEMINI_API_KEY="your-key-here"

streamlit run app.py
```

Then open `http://localhost:8501`.

1. Enter your Gemini API key in the **sidebar**.
2. Click **Rebuild Ledger** (runs extraction pipeline, ~30 sec).
3. Pick a date to see the **Daily Brief**.
4. Switch to the **Q&A** tab to ask questions.

---

## Architecture

```
RAW SOURCES  (transcript · calendars · emails · voice notes)
      │
 [1] INGEST      pipeline/ingest.py
      │  → wrap every source in a common "Utterance" object
      │    {source_id, channel, timestamp, speaker, is_arjun, text}
      ▼
 [2] EXTRACT     pipeline/extract.py  ← Gemini API (LLM)
      │  → structured JSON candidate commitments per utterance
      │  → voice-note rule: Arjun's notes = his own statements
      ▼
 [3] RESOLVE     pipeline/extract.py  (deterministic)
      │  → "tomorrow" / "Wednesday evening" → absolute ISO-8601
      │    anchored to each utterance's own timestamp
      ▼
 [4] DEDUPLICATE pipeline/dedup.py    (deterministic)
      │  → cluster by topic_key
      │  → latest-utterance-timestamp wins on conflicting deadlines
      │  → detect completion signals → mark done
      │  → conflicting ownership → ambiguous_owner flag
      ▼
 [5] CLASSIFY    pipeline/dedup.py    (deterministic)
      │  → open / done / overdue / ambiguous_owner
      │    relative to selected run_date
      ▼
 [6] LEDGER      ledger.json          (JSON file, no database)
      │
   ┌──┴──┐
   ▼     ▼
BRIEF   Q&A          app.py (Streamlit)
date-   read-only
driven  over ledger  ← Gemini API (LLM)
```

**Key design decision:** The LLM only touches two isolated steps — extraction and Q&A phrasing. Everything in between is deterministic Python. This makes deduplication auditable (every claim traces back to a specific source ID) and makes the pipeline testable without an API key.

---

## Data Model (Commitment Ledger Record)

```json
{
  "id": "C-001",
  "topic_key": "vendor_list",
  "description": "Send updated vendor list to Raghav",
  "direction": "arjun_owes",
  "counterparty": "Raghav Sethi",
  "deadline_current": "2026-09-23T09:00:00",
  "deadline_history": [
    {"stated": "today",                     "resolved": "2026-09-21T18:00:00", "source": "transcript#1"},
    {"stated": "tomorrow morning",          "resolved": "2026-09-22T09:00:00", "source": "email#T1-2"},
    {"stated": "tomorrow (Wed) morning",    "resolved": "2026-09-23T09:00:00", "source": "email#T1-4"}
  ],
  "status": "overdue",
  "ambiguous_owner": false,
  "evidence": ["transcript#1", "email#T1-1", "email#T1-2", "email#T1-4", "voicenote#1"],
  "confidence": "high"
}
```

| Field | Purpose |
|---|---|
| `direction` | `arjun_owes` / `arjun_waiting_on` / `fyi` |
| `deadline_history` | Full audit trail of all deadline revisions |
| `status` | `open` / `done` / `overdue` / `ambiguous_owner` |
| `ambiguous_owner` | True = agent refuses to guess the owner |
| `confidence` | `high` / `medium` / `low` — lowest value across all source mentions |
| `evidence` | Source IDs — every claim is traceable |

---

## The 5 Canonical Commitments

| # | Topic | Direction | Final Deadline | Status as of Wed 08:00 |
|---|---|---|---|---|
| C-001 | Vendor list → Raghav | Arjun owes | Wed AM | **Overdue** |
| C-002 | Q3 campaign deck review | Waiting on Neha | Thu 9:30 AM (moved from Wed) | On track |
| C-003 | Reconfirm Meridian call | Arjun owes | — | **Done** (Wed 3PM confirmed) |
| C-004 | Expense variance report | Waiting on Divya | Wed eve (moved earlier from Thu) | **Done** (delivered Wed 18:00) |
| C-005 | Mumbai lease sign-off | **Ambiguous owner** | Fri 25 Sep EOD | Unowned — flagged |

---

## Inputs, Sources & Assumptions

### Sources used
- Meeting transcript — Leadership Sync, Mon 21 Sep 09:00
- 4 participants' calendars (Arjun, Neha, Raghav, Divya), week of 21–25 Sep 2026
- 5 email threads (Vendor List, Q3 Deck, Call Reschedule, Expense Report, Mumbai Lease)
- 2 personal voice notes (Arjun to himself)

### Assumptions
1. **"Today" is a parameter** — the brief date is selected by the user, defaulting to Wed 23 Sep (richest test case).
2. **Voice notes = Arjun's own statements** — per the data pack note. The extraction prompt explicitly instructs the LLM to treat voice note content as Arjun's own commitments, not third-party instructions.
3. **Mumbai lease is deliberately left unowned** — the agent will not infer Facilities, Divya, or Arjun owns it. The data shows all parties explicitly disclaiming ownership.
4. **Message timestamps are ground truth** for resolving relative dates ("tomorrow", "Wednesday evening"). Each utterance's own timestamp is the anchor.
5. **Latest stated deadline wins** — when the same commitment has multiple deadline mentions, the one from the latest message is canonical (but all prior mentions are preserved in `deadline_history`).
6. **Completion detected from email content** — e.g. "Report attached, sent as promised" → status: done.

---

## AI Tools Used

| Tool | How used |
|---|---|
| **Gemini 2.0 Flash** (Google AI) | Step 2: Extraction — structured JSON from unstructured prose. Step 7: Q&A — phrasing natural-language answers grounded in the ledger. |
| **Antigravity IDE** (Google DeepMind) | Code generation, architecture planning, debugging the pipeline. |

---

## Running Tests

```bash
source venv/bin/activate
pytest tests/test_dedup.py -v
```

14 tests covering: deadline resolution (latest-wins), deadline moving earlier, done-signal override, ambiguous owner propagation, evidence union, confidence minimization, status classification edge cases.

---

## Project Structure

```
.
├── app.py                    # Streamlit frontend
├── requirements.txt
├── ledger.json               # Generated by pipeline (gitignored by default)
├── data/
│   └── raw_sources.py        # All source data as Python constants
├── pipeline/
│   ├── ingest.py             # Step 1: Normalization → Utterance objects
│   ├── extract.py            # Steps 2-3: LLM extraction + date resolution
│   ├── dedup.py              # Steps 4-5: Deduplication + classification
│   ├── ledger.py             # Step 6: Pipeline orchestrator + ledger I/O
│   └── qa.py                 # Step 7b: Q&A using ledger as read-only context
└── tests/
    └── test_dedup.py         # 14 pytest tests for the dedup engine
```
