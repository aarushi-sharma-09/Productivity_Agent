# ⚡ ExecBrief — Executive Productivity Agent

> **Assignment 1 · AIONOS Agentic AI Factory**

An AI agent that turns Arjun Malhotra's scattered executive inputs (meeting transcripts, calendars, emails, voice notes) into a clean, deduplicated Daily Action Brief with a Q&A interface.

![React](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-blue) ![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green) ![LLM](https://img.shields.io/badge/LLM-Gemini%203.6%20Flash-yellow)

---

## Live Demo

- **Frontend (Vercel):** *(https://productivity-agent-five.vercel.app/)*
- **Backend (Render):** *https://productivity-agent-k0vi.onrender.com*

---

## One-Command Local Run

This project uses a decoupled React frontend and a Python FastAPI backend. We've included an orchestrator script to run both simultaneously.

```bash
git clone <repo-url>
cd Productivity_Agent

# Ensure you have an API key set up:
# Create a .env file and add: GEMINI_API_KEY="AIzaSy..."

# Start both frontend and backend automatically:
chmod +x start.sh
./start.sh
```

Then open `http://localhost:5173`.

1. Click **Access Agent Dashboard** on the mock SSO screen.
2. The Daily Brief will automatically load the commitments for `2026-09-23`.
3. Switch to the **Q&A** tab to ask questions (e.g. "What did I promise Raghav?").

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
 [6] LEDGER      ledger.json          (JSON file, acting as database)
      │
   ┌──┴──┐
   ▼     ▼
 BRIEF   Q&A          api.py (FastAPI)  ← serves JSON over REST
                      frontend/ (React/Vite UI)
```

**Key design decision:** The LLM only touches two isolated steps — extraction and Q&A phrasing. Everything in between is deterministic Python. This makes deduplication auditable (every claim traces back to a specific source ID) and makes the pipeline testable without requiring an API key.

---

## Tools Used
- **Python / FastAPI:** Core backend logic and REST API.
- **React / Vite / Tailwind CSS:** Consumer-grade glassmorphism frontend interface.
- **Google GenAI SDK (Gemini 3.6 Flash):** Used strictly for raw text extraction and natural language Q&A phrasing.
- **Pytest:** Deterministic unit testing for the deduplication engine.
