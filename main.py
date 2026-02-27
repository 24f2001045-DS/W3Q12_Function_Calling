from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import re
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/execute")
def execute(q: str = Query(...)):
    q = q.strip()

    # 1️⃣ Ticket Status
    ticket_match = re.fullmatch(
        r"What is the status of ticket (\d+)\?",
        q
    )
    if ticket_match:
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({
                "ticket_id": int(ticket_match.group(1))
            })
        }

    # 2️⃣ Schedule Meeting
    meeting_match = re.fullmatch(
        r"Schedule a meeting on (\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2}) in (.+)\.",
        q
    )
    if meeting_match:
        return {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": meeting_match.group(1),
                "time": meeting_match.group(2),
                "meeting_room": meeting_match.group(3)
            })
        }

    # 3️⃣ Expense Balance
    expense_match = re.fullmatch(
        r"Show my expense balance for employee (\d+)\.",
        q
    )
    if expense_match:
        return {
            "name": "get_expense_balance",
            "arguments": json.dumps({
                "employee_id": int(expense_match.group(1))
            })
        }

    # 4️⃣ Performance Bonus
    bonus_match = re.fullmatch(
        r"Calculate performance bonus for employee (\d+) for (\d{4})\.",
        q
    )
    if bonus_match:
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": int(bonus_match.group(1)),
                "current_year": int(bonus_match.group(2))
            })
        }

    # 5️⃣ Office Issue
    issue_match = re.fullmatch(
        r"Report office issue (\d+) for the (.+) department\.",
        q
    )
    if issue_match:
        return {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": int(issue_match.group(1)),
                "department": issue_match.group(2)
            })
        }

    from fastapi import HTTPException
    raise HTTPException(status_code=400, detail="Query not recognized")