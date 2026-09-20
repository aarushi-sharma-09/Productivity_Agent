"""
Executive Productivity Agent — Streamlit App
Full glassmorphism redesign with aurora background, frosted glass cards,
glowing accents, and premium Inter typography.
"""

import sys
import os
from pathlib import Path
from datetime import datetime, date

import streamlit as st
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))

# Load .env file automatically (if present) — keeps API keys out of the UI
load_dotenv(Path(__file__).parent / ".env")

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="ExecBrief — Arjun Malhotra",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Full glassmorphism CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── RESET & ROOT ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    font-family: 'Inter', system-ui, sans-serif !important;
}

/* ── AURORA ANIMATED BACKGROUND ── */
.stApp {
    background: #06060f !important;
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 10% 20%, rgba(99,102,241,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 80% at 90% 10%, rgba(139,92,246,0.14) 0%, transparent 55%),
        radial-gradient(ellipse 70% 50% at 50% 90%, rgba(14,165,233,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 50% 60% at 80% 70%, rgba(236,72,153,0.08) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
    animation: aurora 18s ease infinite alternate;
}

@keyframes aurora {
    0%   { opacity: 0.7; transform: scale(1) rotate(0deg); }
    50%  { opacity: 1;   transform: scale(1.05) rotate(1deg); }
    100% { opacity: 0.8; transform: scale(1) rotate(-1deg); }
}

/* ── SIDEBAR GLASS ── */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.03) !important;
    backdrop-filter: blur(24px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
    box-shadow: 4px 0 40px rgba(0,0,0,0.4) !important;
}

[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

[data-testid="stSidebarContent"] {
    padding: 1.5rem 1rem !important;
}

/* ── MAIN CONTENT AREA ── */
.main .block-container {
    padding: 2rem 2.5rem 3rem !important;
    max-width: 1400px !important;
    position: relative;
    z-index: 1;
}

/* ── TABS ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 14px !important;
    padding: 4px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    gap: 4px !important;
    backdrop-filter: blur(12px) !important;
}

[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 10px !important;
    color: rgba(255,255,255,0.5) !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.2s ease !important;
    border: none !important;
}

[data-testid="stTabs"] [data-baseweb="tab"]:hover {
    background: rgba(255,255,255,0.06) !important;
    color: rgba(255,255,255,0.8) !important;
}

[data-testid="stTabs"] [aria-selected="true"] {
    background: rgba(99,102,241,0.25) !important;
    color: #a5b4fc !important;
    box-shadow: 0 0 20px rgba(99,102,241,0.2) !important;
}

[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
    display: none !important;
}

[data-testid="stTabs"] [data-baseweb="tab-border"] {
    display: none !important;
}

/* ── INPUT FIELDS ── */
[data-testid="stTextInput"] input,
[data-testid="stDateInput"] input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    backdrop-filter: blur(10px) !important;
    transition: all 0.2s ease !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stDateInput"] input:focus {
    border-color: rgba(99,102,241,0.5) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
    outline: none !important;
}

/* ── SELECT BOX ── */
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: rgba(99,102,241,0.2) !important;
    border: 1px solid rgba(99,102,241,0.4) !important;
    border-radius: 10px !important;
    color: #a5b4fc !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    backdrop-filter: blur(10px) !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.01em !important;
}

.stButton > button:hover {
    background: rgba(99,102,241,0.35) !important;
    border-color: rgba(99,102,241,0.6) !important;
    box-shadow: 0 0 20px rgba(99,102,241,0.3), 0 4px 15px rgba(0,0,0,0.3) !important;
    transform: translateY(-1px) !important;
    color: #c7d2fe !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, rgba(99,102,241,0.5), rgba(139,92,246,0.5)) !important;
    border: 1px solid rgba(139,92,246,0.5) !important;
    color: #e0e7ff !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.25) !important;
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, rgba(99,102,241,0.7), rgba(139,92,246,0.7)) !important;
    box-shadow: 0 0 30px rgba(99,102,241,0.4), 0 8px 25px rgba(0,0,0,0.3) !important;
}

/* ── METRICS ── */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    padding: 1rem 1.2rem !important;
    backdrop-filter: blur(12px) !important;
    transition: all 0.2s ease !important;
}

[data-testid="stMetric"]:hover {
    background: rgba(255,255,255,0.07) !important;
    border-color: rgba(255,255,255,0.14) !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2) !important;
}

[data-testid="stMetricLabel"] {
    color: rgba(255,255,255,0.5) !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

[data-testid="stMetricValue"] {
    color: #e2e8f0 !important;
    font-weight: 700 !important;
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(10px) !important;
    overflow: hidden !important;
}

[data-testid="stExpander"] summary {
    color: #a5b4fc !important;
    font-weight: 500 !important;
}

/* ── SPINNER ── */
[data-testid="stSpinner"] {
    color: #a5b4fc !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }

/* ── DIVIDER ── */
hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.06) !important;
    margin: 1rem 0 !important;
}

/* ── GLOBAL TEXT ── */
p, span, div, li { color: #94a3b8; }
h1, h2, h3, h4 { color: #f1f5f9 !important; }

/* ── WARNING/ERROR/SUCCESS ── */
[data-testid="stAlert"] {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(10px) !important;
}

/* ── JSON VIEWER ── */
[data-testid="stJson"] {
    background: rgba(0,0,0,0.3) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
}

/* ── GLASS CARD COMPONENTS (custom HTML) ── */

.glass-card {
    background: rgba(255, 255, 255, 0.04);
    backdrop-filter: blur(20px) saturate(160%);
    -webkit-backdrop-filter: blur(20px) saturate(160%);
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 16px;
    padding: 1.25rem 1.4rem;
    margin-bottom: 0.85rem;
    position: relative;
    overflow: hidden;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 24px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.06);
}

.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent);
}

.glass-card:hover {
    background: rgba(255, 255, 255, 0.07);
    border-color: rgba(255, 255, 255, 0.14);
    box-shadow: 0 8px 40px rgba(0,0,0,0.3), 0 0 0 1px rgba(255,255,255,0.05), inset 0 1px 0 rgba(255,255,255,0.08);
    transform: translateY(-2px);
}

.glass-card.overdue {
    border-left: 3px solid rgba(239,68,68,0.7);
    background: rgba(239,68,68,0.05);
    box-shadow: 0 4px 24px rgba(239,68,68,0.1), inset 0 1px 0 rgba(255,255,255,0.04);
}

.glass-card.open {
    border-left: 3px solid rgba(99,102,241,0.7);
}

.glass-card.done {
    border-left: 3px solid rgba(34,197,94,0.7);
    background: rgba(34,197,94,0.03);
    opacity: 0.85;
}

.glass-card.ambiguous {
    border-left: 3px solid rgba(245,158,11,0.7);
    background: rgba(245,158,11,0.04);
    box-shadow: 0 4px 24px rgba(245,158,11,0.08), inset 0 1px 0 rgba(255,255,255,0.04);
}

.glass-card.waiting {
    border-left: 3px solid rgba(139,92,246,0.7);
    background: rgba(139,92,246,0.03);
}

.glass-card.calendar {
    border-left: 3px solid rgba(14,165,233,0.7);
    background: rgba(14,165,233,0.03);
    padding: 0.85rem 1.2rem;
}

/* ── CARD INTERNALS ── */
.card-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 0.45rem;
    line-height: 1.4;
    display: flex;
    align-items: flex-start;
    gap: 8px;
    flex-wrap: wrap;
}

.card-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
    font-size: 0.78rem;
    color: #64748b;
    margin-top: 6px;
}

.card-meta-item {
    display: flex;
    align-items: center;
    gap: 4px;
}

.card-deadline {
    color: #f59e0b;
    font-weight: 600;
    font-size: 0.78rem;
}

.card-deadline.overdue { color: #f87171; }

.card-evidence {
    font-size: 0.68rem;
    color: rgba(255,255,255,0.2);
    margin-top: 8px;
    font-style: italic;
    letter-spacing: 0.02em;
}

/* ── BADGES ── */
.badge {
    display: inline-flex;
    align-items: center;
    padding: 2px 9px;
    border-radius: 100px;
    font-size: 0.67rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    white-space: nowrap;
}

.badge-overdue  { background: rgba(239,68,68,0.15);  color: #fca5a5; border: 1px solid rgba(239,68,68,0.3); }
.badge-open     { background: rgba(99,102,241,0.15); color: #a5b4fc; border: 1px solid rgba(99,102,241,0.3); }
.badge-done     { background: rgba(34,197,94,0.12);  color: #86efac; border: 1px solid rgba(34,197,94,0.25); }
.badge-ambiguous{ background: rgba(245,158,11,0.15); color: #fcd34d; border: 1px solid rgba(245,158,11,0.3); }
.badge-waiting  { background: rgba(139,92,246,0.15); color: #c4b5fd; border: 1px solid rgba(139,92,246,0.3); }
.badge-high     { background: rgba(34,197,94,0.1);   color: #86efac; border: 1px solid rgba(34,197,94,0.2); }
.badge-medium   { background: rgba(245,158,11,0.1);  color: #fcd34d; border: 1px solid rgba(245,158,11,0.2); }
.badge-low      { background: rgba(239,68,68,0.1);   color: #fca5a5; border: 1px solid rgba(239,68,68,0.2); }

/* ── SECTION HEADERS ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 16px;
    border-radius: 10px;
    margin-bottom: 1rem;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    backdrop-filter: blur(8px);
    border: 1px solid transparent;
}

.sh-action   { background: rgba(99,102,241,0.1);  color: #a5b4fc; border-color: rgba(99,102,241,0.2); }
.sh-overdue  { background: rgba(239,68,68,0.1);   color: #fca5a5; border-color: rgba(239,68,68,0.2); }
.sh-waiting  { background: rgba(139,92,246,0.1);  color: #c4b5fd; border-color: rgba(139,92,246,0.2); }
.sh-ambiguous{ background: rgba(245,158,11,0.1);  color: #fcd34d; border-color: rgba(245,158,11,0.2); }
.sh-done     { background: rgba(34,197,94,0.1);   color: #86efac; border-color: rgba(34,197,94,0.2); }
.sh-calendar { background: rgba(14,165,233,0.1);  color: #7dd3fc; border-color: rgba(14,165,233,0.2); }

.section-count {
    margin-left: auto;
    background: rgba(255,255,255,0.08);
    border-radius: 100px;
    padding: 1px 8px;
    font-size: 0.7rem;
    font-weight: 600;
}

/* ── PAGE HEADER ── */
.page-header {
    margin-bottom: 1.5rem;
}

.page-title {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #e2e8f0 0%, #a5b4fc 50%, #c4b5fd 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
    margin-bottom: 4px;
}

.page-subtitle {
    font-size: 0.85rem;
    color: rgba(255,255,255,0.35);
    font-weight: 400;
    letter-spacing: 0.02em;
}

/* ── SIDEBAR HEADER ── */
.sidebar-brand {
    text-align: center;
    padding: 1rem 0 1.5rem;
}

.sidebar-logo {
    font-size: 2.2rem;
    display: block;
    margin-bottom: 6px;
    filter: drop-shadow(0 0 20px rgba(99,102,241,0.6));
    animation: pulse-glow 3s ease infinite;
}

@keyframes pulse-glow {
    0%, 100% { filter: drop-shadow(0 0 16px rgba(99,102,241,0.5)); }
    50%       { filter: drop-shadow(0 0 28px rgba(139,92,246,0.7)); }
}

.sidebar-title {
    font-size: 1.1rem;
    font-weight: 700;
    background: linear-gradient(135deg, #a5b4fc, #c4b5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.sidebar-sub {
    font-size: 0.7rem;
    color: rgba(255,255,255,0.3) !important;
    margin-top: 2px;
}

.sidebar-user-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 0.85rem 1rem;
    margin: 0.5rem 0 1rem;
    backdrop-filter: blur(12px);
}

.sidebar-user-name {
    font-weight: 600;
    font-size: 0.9rem;
    color: #e2e8f0 !important;
}

.sidebar-user-role {
    font-size: 0.73rem;
    color: rgba(255,255,255,0.35) !important;
    margin-top: 2px;
}

/* ── CHAT MESSAGES ── */
.chat-user {
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 14px 14px 4px 14px;
    padding: 0.85rem 1.1rem;
    margin-bottom: 0.7rem;
    backdrop-filter: blur(12px);
}

.chat-ai {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 4px 14px 14px 14px;
    padding: 0.85rem 1.1rem;
    margin-bottom: 0.7rem;
    backdrop-filter: blur(12px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.chat-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 5px;
}

.chat-label.user { color: rgba(165,180,252,0.7); }
.chat-label.ai   { color: rgba(196,181,253,0.7); }

.chat-text { font-size: 0.9rem; color: #cbd5e1; line-height: 1.6; }

/* ── QUICK Q BUTTONS ── */
.quick-q-btn {
    display: inline-block;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 100px;
    padding: 5px 14px;
    font-size: 0.78rem;
    color: rgba(255,255,255,0.5);
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
    backdrop-filter: blur(8px);
}

.quick-q-btn:hover {
    background: rgba(99,102,241,0.15);
    border-color: rgba(99,102,241,0.3);
    color: #a5b4fc;
}

/* ── DEADLINE HISTORY PILL ── */
.dl-history {
    margin-top: 8px;
    padding: 8px 12px;
    background: rgba(0,0,0,0.2);
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.05);
}

.dl-history-row {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.71rem;
    color: rgba(255,255,255,0.3);
    padding: 2px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}

.dl-history-row:last-child { border-bottom: none; }

/* ── EMPTY STATE ── */
.empty-state {
    text-align: center;
    padding: 2rem;
    color: rgba(255,255,255,0.2);
    font-size: 0.85rem;
}

/* ── LEDGER STAT ROW ── */
.ledger-stat {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 0.6rem 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.8rem;
    color: rgba(255,255,255,0.4);
    backdrop-filter: blur(8px);
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Helper rendering functions
# ---------------------------------------------------------------------------

def fmt_deadline(deadline_iso):
    if not deadline_iso:
        return None
    try:
        dt = datetime.fromisoformat(deadline_iso)
        return dt.strftime("%-d %b · %-I:%M %p")
    except Exception:
        return deadline_iso


def render_badge(label, kind):
    return f'<span class="badge badge-{kind}">{label}</span>'


def render_card(c):
    status = c.get("status", "open")
    direction = c.get("direction", "")
    confidence = c.get("confidence", "medium")
    dl_current = c.get("deadline_current")
    dl_history = c.get("deadline_history", [])
    evidence = c.get("evidence", [])
    desc = c.get("description", "Unknown commitment")
    counterparty = c.get("counterparty", "—")
    ambiguous = c.get("ambiguous_owner", False)

    # Badge labels
    status_map = {
        "open": ("Open", "open"),
        "done": ("Done", "done"),
        "overdue": ("Overdue", "overdue"),
        "ambiguous_owner": ("Owner Unclear", "ambiguous"),
    }
    dir_map = {
        "arjun_owes": ("↑ My action", "🔵"),
        "arjun_waiting_on": ("↓ Waiting on", "🟣"),
        "fyi": ("ℹ FYI", "⚪"),
    }
    sl, sk = status_map.get(status, (status, "open"))
    dir_label, dir_icon = dir_map.get(direction, (direction, ""))

    card_class = {"overdue": "overdue", "done": "done",
                  "ambiguous_owner": "ambiguous"}.get(status,
                  "waiting" if direction == "arjun_waiting_on" else "open")

    # Deadline display
    dl_str = fmt_deadline(dl_current)
    dl_class = "overdue" if status == "overdue" else ""

    # Deadline history
    hist_html = ""
    if len(dl_history) > 1:
        rows = ""
        for h in dl_history:
            src = h.get("source", "?")
            stated = h.get("stated", "?")
            resolved = (h.get("resolved") or "")[:10]
            rows += f'<div class="dl-history-row"><span>↪</span><span>"{stated}"</span><span style="color:rgba(255,255,255,0.15)">→</span><span>{resolved}</span><span style="margin-left:auto;color:rgba(255,255,255,0.2)">{src}</span></div>'
        hist_html = f'<div class="dl-history"><div style="font-size:0.65rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:rgba(255,255,255,0.25);margin-bottom:4px;">Deadline history ({len(dl_history)} revisions)</div>{rows}</div>'

    ev_html = f'<div class="card-evidence">Sources: {" · ".join(evidence)}</div>' if evidence else ""

    ambiguous_html = '<div style="margin-top:6px;font-size:0.75rem;color:#fbbf24;display:flex;align-items:center;gap:5px;">⚠️ Ownership unresolved — not assigned to any party</div>' if ambiguous else ""

    html = f"""
<div class="glass-card {card_class}">
  <div class="card-title">
    <span>{desc}</span>
    {render_badge(sl, sk)}
    {render_badge(confidence, confidence)}
  </div>
  <div class="card-meta">
    <span class="card-meta-item">{dir_icon} <span>{dir_label}</span></span>
    <span class="card-meta-item" style="color:#475569">·</span>
    <span class="card-meta-item">👤 <span>{counterparty}</span></span>
    {"<span class='card-meta-item' style='color:#475569'>·</span><span class='card-deadline " + dl_class + "'>🗓 " + dl_str + "</span>" if dl_str else ""}
  </div>
  {ambiguous_html}
  {hist_html}
  {ev_html}
</div>"""
    st.markdown(html, unsafe_allow_html=True)


def section_header(icon, title, count, kind):
    st.markdown(
        f'<div class="section-header sh-{kind}">'
        f'<span>{icon}</span><span>{title}</span>'
        f'<span class="section-count">{count}</span></div>',
        unsafe_allow_html=True,
    )


def empty_state(msg):
    st.markdown(f'<div class="empty-state">{msg}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <span class="sidebar-logo">⚡</span>
        <div class="sidebar-title">ExecBrief</div>
        <div class="sidebar-sub">Executive Productivity Agent</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-user-card">
        <div class="sidebar-user-name">Arjun Malhotra</div>
        <div class="sidebar-user-role">VP Sales · Veridian Corp</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.7rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:rgba(255,255,255,0.25);margin-bottom:8px;">Brief Date</div>', unsafe_allow_html=True)

    selected_date = st.date_input(
        "Brief Date",
        value=date(2026, 9, 23),
        min_value=date(2026, 9, 21),
        max_value=date(2026, 9, 25),
        label_visibility="collapsed",
    )
    run_dt = datetime.combine(selected_date, datetime.min.time()).replace(hour=8)

    st.markdown('<hr/>', unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.7rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:rgba(255,255,255,0.25);margin-bottom:8px;">Pipeline</div>', unsafe_allow_html=True)

    # Show key status — green if loaded from .env, fallback input if not
    if os.environ.get("GEMINI_API_KEY"):
        st.markdown(
            '<div style="background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.25);'
            'border-radius:8px;padding:6px 12px;font-size:0.75rem;color:#86efac;">'
            '🔑 API key loaded from <code style="color:#4ade80">.env</code></div>',
            unsafe_allow_html=True,
        )
    else:
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="AIzaSy...  (or add to .env)",
            label_visibility="collapsed",
            help="Paste your key here, or add GEMINI_API_KEY=... to a .env file in the project root.",
        )
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key

    rebuild = st.button("🔄 Rebuild Ledger", use_container_width=True, type="primary")
    if rebuild:
        if not os.environ.get("GEMINI_API_KEY"):
            st.error("Enter your Gemini API key above first.")
        else:
            try:
                with st.spinner("Running pipeline…"):
                    from pipeline.ledger import build_ledger
                    build_ledger(run_date=run_dt, force_rebuild=True)
                st.success("✅ Ledger rebuilt!")
                st.rerun()
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    err_title = "API Rate Limit Exceeded"
                    err_desc = "You hit the Gemini free tier quota (5 requests per minute). The pipeline automatically retries, but if it fails completely, wait 60 seconds and try again."
                elif "400" in err_str or "API_KEY_INVALID" in err_str:
                    err_title = "Invalid API Key"
                    err_desc = "The API key provided is not valid. Make sure you copied it correctly from Google AI Studio (it should start with AIzaSy)."
                elif "404" in err_str:
                    err_title = "Model Not Found"
                    err_desc = "The requested model is deprecated. Please check extract.py and qa.py to ensure MODEL_NAME is set to a valid model (like gemini-2.5-flash)."
                else:
                    err_title = "Pipeline Error"
                    err_desc = "An unexpected error occurred during extraction."

                st.markdown(f'''
                <div class="glass-card overdue" style="margin-top:1rem; border-left:4px solid #ef4444;">
                    <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                        <span style="font-size:1.4rem;">⚠️</span>
                        <span style="font-weight:700; color:#fca5a5; font-size:1.05rem;">{err_title}</span>
                    </div>
                    <div style="color:#e2e8f0; font-size:0.85rem; margin-bottom:12px; line-height:1.5;">
                        {err_desc}
                    </div>
                    <div style="background:rgba(0,0,0,0.3); border-radius:6px; padding:8px 12px; font-family:monospace; font-size:0.7rem; color:rgba(255,255,255,0.5); word-break:break-all;">
                        {err_str}
                    </div>
                </div>
                ''', unsafe_allow_html=True)

    st.markdown('<hr/>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:0.67rem;color:rgba(255,255,255,0.2);text-align:center;line-height:1.8;">'
        'Week of 21–25 Sep 2026<br>LLM: Gemini 2.5 Flash<br>Deterministic dedup engine</div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
try:
    from pipeline.ledger import load_ledger, get_commitments_for_date
    brief_data = get_commitments_for_date(run_dt)
    ledger_data = load_ledger(run_date=run_dt)
    has_ledger = True
except FileNotFoundError:
    has_ledger = False
    brief_data = {}
    ledger_data = {}


# ---------------------------------------------------------------------------
# TABS
# ---------------------------------------------------------------------------
tab_brief, tab_qa, tab_ledger = st.tabs(["📋  Daily Brief", "💬  Ask Arjun", "🗂  Full Ledger"])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 1 — DAILY BRIEF
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_brief:
    st.markdown(f"""
    <div class="page-header">
        <div class="page-title">Daily Brief</div>
        <div class="page-subtitle">{run_dt.strftime("%A, %d %B %Y")} · Arjun Malhotra</div>
    </div>
    """, unsafe_allow_html=True)

    if not has_ledger:
        st.markdown("""
        <div class="glass-card ambiguous" style="text-align:center;padding:2.5rem;">
            <div style="font-size:2rem;margin-bottom:12px;">🔒</div>
            <div style="font-size:1rem;font-weight:600;color:#e2e8f0;margin-bottom:8px;">No ledger found</div>
            <div style="font-size:0.85rem;color:rgba(255,255,255,0.35);">
                Enter your Gemini API key in the sidebar and click <strong style="color:#a5b4fc">Rebuild Ledger</strong> to run the extraction pipeline.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # ── Metric row ──
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            n_action = len(brief_data.get("my_actions", [])) + len(brief_data.get("overdue", []))
            st.metric("My Actions", n_action)
        with m2:
            st.metric("🔴 Overdue", len(brief_data.get("overdue", [])))
        with m3:
            st.metric("🟣 Waiting On", len(brief_data.get("waiting_on", [])))
        with m4:
            st.metric("🟠 Needs Owner", len(brief_data.get("ambiguous", [])))

        st.markdown("<hr/>", unsafe_allow_html=True)

        left_col, right_col = st.columns([3, 2], gap="large")

        with left_col:
            # Overdue
            overdue = brief_data.get("overdue", [])
            if overdue:
                section_header("🔴", "Overdue", len(overdue), "overdue")
                for c in overdue:
                    render_card(c)
                st.markdown("<hr/>", unsafe_allow_html=True)

            # My Actions
            my_actions = brief_data.get("my_actions", [])
            section_header("🔵", "My Actions Today", len(my_actions), "action")
            if my_actions:
                for c in my_actions:
                    render_card(c)
            else:
                empty_state("No actions due today.")

            st.markdown("<hr/>", unsafe_allow_html=True)

            # Waiting on others
            waiting = brief_data.get("waiting_on", [])
            section_header("🟣", "Waiting On Others", len(waiting), "waiting")
            if waiting:
                for c in waiting:
                    render_card(c)
            else:
                empty_state("Nothing waiting on others.")

            # Done
            done = brief_data.get("done", [])
            if done:
                st.markdown("<hr/>", unsafe_allow_html=True)
                section_header("✅", "Completed", len(done), "done")
                for c in done:
                    render_card(c)

        with right_col:
            # Needs ownership — top priority in right column
            ambiguous = brief_data.get("ambiguous", [])
            section_header("🟠", "Needs Ownership", len(ambiguous), "ambiguous")
            if ambiguous:
                for c in ambiguous:
                    render_card(c)
            else:
                empty_state("No unowned items.")

            st.markdown("<hr/>", unsafe_allow_html=True)

            # Calendar
            cal = brief_data.get("calendar_today", [])
            section_header("📅", "Today's Calendar", len(cal), "calendar")
            if cal:
                for ev in cal:
                    st.markdown(
                        f'<div class="glass-card calendar">'
                        f'<div class="card-title" style="font-size:0.88rem;">{ev["event"]}</div>'
                        f'<div class="card-meta"><span>🕐 {ev["time"]}</span></div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
            else:
                empty_state("No calendar events today.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 2 — Q&A
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_qa:
    st.markdown("""
    <div class="page-header">
        <div class="page-title">Ask About Your Commitments</div>
        <div class="page-subtitle">Answers grounded in your ledger — never hallucinated.</div>
    </div>
    """, unsafe_allow_html=True)

    # Suggested questions as pill buttons
    suggested_qs = [
        "What did I promise Raghav?",
        "What needs action today?",
        "Who owns the Mumbai lease?",
        "Is the expense report done?",
        "Did the deck deadline change?",
        "What's overdue?",
    ]

    st.markdown('<div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:1.2rem;">', unsafe_allow_html=True)
    cols = st.columns(len(suggested_qs))
    for i, q in enumerate(suggested_qs):
        if cols[i].button(q, key=f"sq_{i}", use_container_width=True):
            st.session_state["qa_prefill"] = q
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)

    # Chat history
    if "chat" not in st.session_state:
        st.session_state["chat"] = []

    for msg in st.session_state["chat"]:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="chat-user">'
                f'<div class="chat-label user">You</div>'
                f'<div class="chat-text">{msg["content"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="chat-ai">'
                f'<div class="chat-label ai">⚡ ExecBrief</div>'
                f'<div class="chat-text">{msg["content"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # Input row
    input_col, send_col, clear_col = st.columns([7, 1, 1])
    with input_col:
        prefill = st.session_state.pop("qa_prefill", "")
        user_q = st.text_input(
            "Ask a question",
            value=prefill,
            placeholder="e.g. What did I promise Raghav?",
            label_visibility="collapsed",
            key="qa_input",
        )
    with send_col:
        send = st.button("Send", type="primary", use_container_width=True)
    with clear_col:
        if st.button("Clear", use_container_width=True):
            st.session_state["chat"] = []
            st.rerun()

    if send and user_q.strip():
        if not has_ledger:
            st.warning("Rebuild the ledger first.")
        elif not os.environ.get("GEMINI_API_KEY"):
            st.error("Enter your Gemini API key in the sidebar.")
        else:
            from pipeline.qa import answer_question
            with st.spinner("Thinking…"):
                answer = answer_question(user_q.strip(), ledger_data)
            st.session_state["chat"].append({"role": "user", "content": user_q.strip()})
            st.session_state["chat"].append({"role": "assistant", "content": answer})
            st.rerun()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 3 — FULL LEDGER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_ledger:
    st.markdown("""
    <div class="page-header">
        <div class="page-title">Commitment Ledger</div>
        <div class="page-subtitle">All canonical commitments — extracted, deduplicated, classified.</div>
    </div>
    """, unsafe_allow_html=True)

    if not has_ledger:
        empty_state("No ledger found. Rebuild from the sidebar.")
    else:
        commitments = ledger_data.get("commitments", [])

        st.markdown(
            f'<div class="ledger-stat">Generated: {ledger_data.get("generated_at","—")} &nbsp;·&nbsp; '
            f'<strong style="color:#a5b4fc">{len(commitments)}</strong> canonical commitments after deduplication</div>',
            unsafe_allow_html=True,
        )

        f1, f2 = st.columns(2)
        status_f = f1.selectbox("Filter by status", ["All", "open", "overdue", "done", "ambiguous_owner"])
        dir_f = f2.selectbox("Filter by direction", ["All", "arjun_owes", "arjun_waiting_on", "fyi"])

        filtered = commitments
        if status_f != "All":
            filtered = [c for c in filtered if c.get("status") == status_f]
        if dir_f != "All":
            filtered = [c for c in filtered if c.get("direction") == dir_f]

        st.markdown(
            f'<div style="font-size:0.75rem;color:rgba(255,255,255,0.25);margin-bottom:1rem;">{len(filtered)} record(s) shown</div>',
            unsafe_allow_html=True,
        )

        for c in filtered:
            cid = c.get("id", "?")
            cdesc = c.get("description", "—")
            with st.expander(f"[{cid}]  {cdesc}", expanded=False):
                render_card(c)
                st.json(c)
