"""
Raw source data for the Executive Productivity Agent.
Week: Monday 21 September 2026 – Friday 25 September 2026.
Agent user: Arjun Malhotra (VP Sales).
"""

# ---------------------------------------------------------------------------
# 1. Meeting Transcript
# ---------------------------------------------------------------------------
TRANSCRIPT = {
    "source_id": "transcript#1",
    "channel": "transcript",
    "timestamp": "2026-09-21T09:00:00",
    "speaker": "multiple",
    "text": (
        "Attendees: Arjun Malhotra, Neha Kapoor, Raghav Sethi, Divya Rao. "
        "Arjun: Let's keep this quick. Neha, where are we on the Q3 campaign deck? "
        "Neha: Draft is 80% done. I'll send it to Arjun for review by Wednesday. "
        "Arjun: Good. Also, remind me — I told Raghav I'd send him the updated vendor list. "
        "I'll get that to him by end of day tomorrow. "
        "Raghav: Appreciated. Separately, the Mumbai office renewal paperwork needs someone "
        "to sign off this week. Not sure whose desk that's on right now. "
        "Divya: I think that's supposed to be Facilities, but I haven't seen anyone pick it up. "
        "Arjun: Okay, flag it, don't assume. Divya, can you also pull the July expense variance "
        "report before Thursday's board prep? "
        "Divya: Yes, I'll have it ready Wednesday evening. "
        "Arjun: One more thing — client call with Meridian Logistics got pushed. I need to "
        "reconfirm the new time with their team myself. "
        "Neha: Also, just a reminder, the campaign deck review — I said Wednesday, but "
        "realistically Thursday morning is safer. "
        "Arjun: Noted. Let's close here."
    ),
}

# ---------------------------------------------------------------------------
# 2. Calendars
# ---------------------------------------------------------------------------
CALENDARS = {
    "Arjun Malhotra": [
        {"date": "2026-09-21", "time": "09:00-09:35", "event": "Leadership Sync"},
        {"date": "2026-09-21", "time": "14:00-14:30", "event": "1:1 with Neha"},
        {"date": "2026-09-21", "time": "16:00-17:00", "event": "Blocked"},
        {"date": "2026-09-22", "time": "11:00-12:00", "event": "Internal Budget Review"},
        {"date": "2026-09-22", "time": "15:00-15:30", "event": "Blocked"},
        {"date": "2026-09-23", "time": "15:00-15:30", "event": "Call — Meridian Logistics"},
        {"date": "2026-09-23", "time": "18:00-18:15", "event": "Blocked"},
        {"date": "2026-09-24", "time": "09:00-10:00", "event": "Board Prep Session"},
        {"date": "2026-09-24", "time": "16:00-17:00", "event": "Hiring Panel — Sales Associate"},
        {"date": "2026-09-25", "time": "10:00-10:30", "event": "Facilities Check-in"},
        {"date": "2026-09-25", "time": "13:00-14:00", "event": "Blocked"},
    ],
    "Neha Kapoor": [
        {"date": "2026-09-21", "time": "10:00-11:00", "event": "Blocked"},
        {"date": "2026-09-21", "time": "14:00-14:30", "event": "1:1 with Arjun"},
        {"date": "2026-09-22", "time": "13:00-14:00", "event": "Campaign Vendor Call"},
        {"date": "2026-09-23", "time": "10:00-10:30", "event": "Deck Prep"},
        {"date": "2026-09-23", "time": "13:00-15:00", "event": "Blocked"},
        {"date": "2026-09-24", "time": "09:30-10:00", "event": "Deck Review with Arjun"},
        {"date": "2026-09-25", "time": "11:00-12:00", "event": "Blocked"},
    ],
    "Raghav Sethi": [
        {"date": "2026-09-21", "time": "09:00-09:35", "event": "Leadership Sync"},
        {"date": "2026-09-21", "time": "13:00-14:00", "event": "Blocked"},
        {"date": "2026-09-22", "time": "11:00-12:00", "event": "Internal Budget Review"},
        {"date": "2026-09-22", "time": "15:30-16:00", "event": "Ops Standup"},
        {"date": "2026-09-23", "time": "09:00-11:00", "event": "Blocked"},
        {"date": "2026-09-24", "time": "14:00-15:00", "event": "Blocked"},
        {"date": "2026-09-25", "time": "10:00-10:30", "event": "Facilities Check-in"},
        {"date": "2026-09-25", "time": "15:00-16:00", "event": "Blocked"},
    ],
    "Divya Rao": [
        {"date": "2026-09-21", "time": "14:30-15:00", "event": "Budget Prep"},
        {"date": "2026-09-21", "time": "16:00-17:00", "event": "Blocked"},
        {"date": "2026-09-22", "time": "09:00-09:15", "event": "Quick Call with Arjun"},
        {"date": "2026-09-22", "time": "11:00-12:00", "event": "Internal Budget Review"},
        {"date": "2026-09-23", "time": "13:00-14:00", "event": "Blocked"},
        {"date": "2026-09-24", "time": "09:00-10:00", "event": "Board Prep Session"},
        {"date": "2026-09-24", "time": "14:00-15:00", "event": "Blocked"},
        {"date": "2026-09-25", "time": "10:00-11:00", "event": "Blocked"},
    ],
}

# ---------------------------------------------------------------------------
# 3. Email Threads
# ---------------------------------------------------------------------------
EMAIL_THREADS = [
    {
        "thread_id": "T1",
        "subject": "Vendor List",
        "emails": [
            {
                "source_id": "email#T1-1",
                "timestamp": "2026-09-21T09:50:00",
                "from": "raghav.sethi@veridian-corp.example",
                "to": "arjun.malhotra@veridian-corp.example",
                "body": "Following up from the sync — can you send the updated vendor list today?",
            },
            {
                "source_id": "email#T1-2",
                "timestamp": "2026-09-21T17:40:00",
                "from": "arjun.malhotra@veridian-corp.example",
                "to": "raghav.sethi@veridian-corp.example",
                "body": "Running behind, will send first thing tomorrow morning instead.",
            },
            {
                "source_id": "email#T1-3",
                "timestamp": "2026-09-22T09:15:00",
                "from": "raghav.sethi@veridian-corp.example",
                "to": "arjun.malhotra@veridian-corp.example",
                "body": "No worries, whenever you get a chance today works.",
            },
            {
                "source_id": "email#T1-4",
                "timestamp": "2026-09-22T18:30:00",
                "from": "arjun.malhotra@veridian-corp.example",
                "to": "raghav.sethi@veridian-corp.example",
                "body": "Sorry, got pulled into board prep — will send by tomorrow (Wednesday) morning for sure.",
            },
            {
                "source_id": "email#T1-5",
                "timestamp": "2026-09-23T08:45:00",
                "from": "raghav.sethi@veridian-corp.example",
                "to": "arjun.malhotra@veridian-corp.example",
                "body": "Just checking — still good for this morning?",
            },
        ],
    },
    {
        "thread_id": "T2",
        "subject": "Q3 Campaign Deck",
        "emails": [
            {
                "source_id": "email#T2-1",
                "timestamp": "2026-09-21T11:00:00",
                "from": "neha.kapoor@veridian-corp.example",
                "to": "arjun.malhotra@veridian-corp.example",
                "body": "Deck's coming together, still targeting Wednesday for your review.",
            },
            {
                "source_id": "email#T2-2",
                "timestamp": "2026-09-22T16:15:00",
                "from": "neha.kapoor@veridian-corp.example",
                "to": "arjun.malhotra@veridian-corp.example",
                "body": "Heads up — shifting the review to Thursday morning instead of Wednesday, need one more day on the data slides.",
            },
            {
                "source_id": "email#T2-3",
                "timestamp": "2026-09-23T10:00:00",
                "from": "arjun.malhotra@veridian-corp.example",
                "to": "neha.kapoor@veridian-corp.example",
                "body": "Understood, Thursday morning works. What time exactly?",
            },
            {
                "source_id": "email#T2-4",
                "timestamp": "2026-09-23T10:20:00",
                "from": "neha.kapoor@veridian-corp.example",
                "to": "arjun.malhotra@veridian-corp.example",
                "body": "Let's say 9:30 AM Thursday, before your board prep block.",
            },
            {
                "source_id": "email#T2-5",
                "timestamp": "2026-09-24T08:00:00",
                "from": "neha.kapoor@veridian-corp.example",
                "to": "arjun.malhotra@veridian-corp.example",
                "body": "Deck is ready, attaching the draft ahead of our 9:30 review.",
            },
        ],
    },
    {
        "thread_id": "T3",
        "subject": "Call Reschedule",
        "emails": [
            {
                "source_id": "email#T3-1",
                "timestamp": "2026-09-21T13:00:00",
                "from": "priya.nair@meridianlogistics.example",
                "to": "arjun.malhotra@veridian-corp.example",
                "body": "Our scheduled call this week got bumped from our side — can you propose a new time? We're flexible Tuesday–Thursday afternoons.",
            },
            {
                "source_id": "email#T3-2",
                "timestamp": "2026-09-22T15:00:00",
                "from": "arjun.malhotra@veridian-corp.example",
                "to": "priya.nair@meridianlogistics.example",
                "body": "Apologies for the delay — how about Wednesday 3:00 PM?",
            },
            {
                "source_id": "email#T3-3",
                "timestamp": "2026-09-22T17:45:00",
                "from": "priya.nair@meridianlogistics.example",
                "to": "arjun.malhotra@veridian-corp.example",
                "body": "Wednesday 3 PM works on our end, confirmed.",
            },
            {
                "source_id": "email#T3-4",
                "timestamp": "2026-09-23T13:30:00",
                "from": "priya.nair@meridianlogistics.example",
                "to": "arjun.malhotra@veridian-corp.example",
                "body": "Quick check — still on for 3 PM today?",
            },
            {
                "source_id": "email#T3-5",
                "timestamp": "2026-09-23T14:00:00",
                "from": "arjun.malhotra@veridian-corp.example",
                "to": "priya.nair@meridianlogistics.example",
                "body": "Yes, confirmed, see you at 3.",
            },
        ],
    },
    {
        "thread_id": "T4",
        "subject": "Expense Variance Report",
        "emails": [
            {
                "source_id": "email#T4-1",
                "timestamp": "2026-09-21T14:30:00",
                "from": "divya.rao@veridian-corp.example",
                "to": "arjun.malhotra@veridian-corp.example",
                "body": "Starting on the July variance numbers, targeting Thursday morning for board prep as discussed.",
            },
            {
                "source_id": "email#T4-2",
                "timestamp": "2026-09-22T09:00:00",
                "from": "arjun.malhotra@veridian-corp.example",
                "to": "divya.rao@veridian-corp.example",
                "body": "Actually, can I get it by Wednesday evening instead? Want time to review before Thursday.",
            },
            {
                "source_id": "email#T4-3",
                "timestamp": "2026-09-22T09:40:00",
                "from": "divya.rao@veridian-corp.example",
                "to": "arjun.malhotra@veridian-corp.example",
                "body": "Wednesday evening is tight but doable, I'll prioritize it.",
            },
            {
                "source_id": "email#T4-4",
                "timestamp": "2026-09-23T18:00:00",
                "from": "divya.rao@veridian-corp.example",
                "to": "arjun.malhotra@veridian-corp.example",
                "body": "Report attached, sent as promised.",
            },
            {
                "source_id": "email#T4-5",
                "timestamp": "2026-09-23T18:10:00",
                "from": "arjun.malhotra@veridian-corp.example",
                "to": "divya.rao@veridian-corp.example",
                "body": "Got it, thank you — exactly what I needed before tomorrow.",
            },
        ],
    },
    {
        "thread_id": "T5",
        "subject": "Mumbai Office Lease Renewal",
        "emails": [
            {
                "source_id": "email#T5-1",
                "timestamp": "2026-09-21T10:15:00",
                "from": "facilities@veridian-corp.example",
                "to": "all-staff@veridian-corp.example",
                "body": "Reminder: the Mumbai office lease renewal requires an authorized signature by Friday, 25 September.",
            },
            {
                "source_id": "email#T5-2",
                "timestamp": "2026-09-22T11:00:00",
                "from": "raghav.sethi@veridian-corp.example",
                "to": "arjun.malhotra@veridian-corp.example",
                "body": "Following up from the sync — has anyone confirmed who's signing off on the Mumbai renewal? Don't think it's been assigned.",
            },
            {
                "source_id": "email#T5-3",
                "timestamp": "2026-09-23T09:30:00",
                "from": "divya.rao@veridian-corp.example",
                "to": "raghav.sethi@veridian-corp.example",
                "body": "Not on my end — I believe this typically sits with Facilities directly, not us.",
            },
            {
                "source_id": "email#T5-4",
                "timestamp": "2026-09-24T16:00:00",
                "from": "facilities@veridian-corp.example",
                "to": "all-staff@veridian-corp.example",
                "body": "Second reminder: signature is still pending. Deadline is Friday, 25 September, end of day.",
            },
            {
                "source_id": "email#T5-5",
                "timestamp": "2026-09-24T16:45:00",
                "from": "raghav.sethi@veridian-corp.example",
                "to": "arjun.malhotra@veridian-corp.example",
                "body": "This is now one day out and still unowned — can you confirm who's handling it?",
            },
        ],
    },
]

# ---------------------------------------------------------------------------
# 4. Voice Notes
# ---------------------------------------------------------------------------
VOICE_NOTES = [
    {
        "source_id": "voicenote#1",
        "channel": "voice_note",
        "timestamp": "2026-09-21T18:40:00",
        "speaker": "Arjun Malhotra",
        "text": (
            "Quick note to self — need to get Raghav that vendor list, I think I said today "
            "but it might slip to tomorrow morning, remind me. Also still haven't heard back "
            "on the Mumbai lease thing, someone needs to own that, I don't think it's me."
        ),
    },
    {
        "source_id": "voicenote#2",
        "channel": "voice_note",
        "timestamp": "2026-09-23T08:15:00",
        "speaker": "Arjun Malhotra",
        "text": (
            "Reminder — expense variance report from Divya needs to be in my hands by "
            "Wednesday evening, not Thursday, I want time to go through it before board prep. "
            "Also Meridian call — I owe Priya a time, need to lock that in today."
        ),
    },
]

# ---------------------------------------------------------------------------
# People registry
# ---------------------------------------------------------------------------
PEOPLE = {
    "arjun.malhotra@veridian-corp.example": "Arjun Malhotra",
    "neha.kapoor@veridian-corp.example": "Neha Kapoor",
    "raghav.sethi@veridian-corp.example": "Raghav Sethi",
    "divya.rao@veridian-corp.example": "Divya Rao",
    "priya.nair@meridianlogistics.example": "Priya Nair",
    "facilities@veridian-corp.example": "Facilities",
    "all-staff@veridian-corp.example": "All Staff",
}

ARJUN_EMAIL = "arjun.malhotra@veridian-corp.example"
