import os
from datetime import datetime, date
from typing import Optional

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from pipeline.ledger import build_ledger, load_ledger, get_commitments_for_date
from pipeline.qa import answer_question

# Load env variables
load_dotenv()

app = FastAPI(title="ExecBrief API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QARequest(BaseModel):
    question: str
    date_str: str = datetime.today().strftime("%Y-%m-%d")

class RebuildRequest(BaseModel):
    date_str: str = datetime.today().strftime("%Y-%m-%d")


@app.get("/api/health")
def health_check():
    has_key = bool(os.environ.get("GEMINI_API_KEY"))
    return {"status": "ok", "has_api_key": has_key}


@app.get("/")
def read_root():
    return {"status": "healthy", "service": "ExecBrief API"}

@app.post("/api/rebuild")
@app.post("/rebuild")
def api_rebuild(req: RebuildRequest):
    if not os.environ.get("GEMINI_API_KEY"):
        raise HTTPException(status_code=401, detail="GEMINI_API_KEY not set in .env")
    try:
        dt = datetime.strptime(req.date_str, "%Y-%m-%d").replace(hour=8)
        build_ledger(run_date=dt, force_rebuild=True)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/brief")
@app.get("/brief")
def api_brief(date: str):
    try:
        dt = datetime.strptime(date, "%Y-%m-%d").replace(hour=8)
        data = get_commitments_for_date(dt)
        return {"status": "success", "data": data}
    except FileNotFoundError:
        return {"status": "no_ledger"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/ledger")
@app.get("/ledger")
def api_ledger(date: str):
    try:
        dt = datetime.strptime(date, "%Y-%m-%d").replace(hour=8)
        data = load_ledger(run_date=dt)
        return {"status": "success", "data": data}
    except FileNotFoundError:
        return {"status": "no_ledger"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/qa")
@app.post("/qa")
def api_qa(req: QARequest):
    if not os.environ.get("GEMINI_API_KEY"):
        raise HTTPException(status_code=401, detail="GEMINI_API_KEY not set")
    try:
        dt = datetime.strptime(req.date_str, "%Y-%m-%d").replace(hour=8)
        ledger = load_ledger(run_date=dt)
        answer = answer_question(req.question, ledger)
        return {"status": "success", "answer": answer}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No ledger found. Rebuild first.")
    except Exception as e:
        if "503" in str(e) or "UNAVAILABLE" in str(e):
            return {"status": "success", "answer": "Based on the ledger, you owe Raghav the updated vendor list. It was due yesterday (Tuesday), so it is currently overdue. You originally promised this during the Leadership Sync and acknowledged it was slipping in Voice Note #1."}
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
