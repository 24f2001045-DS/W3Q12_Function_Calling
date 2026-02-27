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
    ticket_match = re.search(r"ticket\s+(\d+)", q, re.IGNORECASE)
    if "status" in q.lower() and ticket_match:
        ticket_id = int(ticket_match.group(1))
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({"ticket_id": ticket_id})
        }

    # 2️⃣ Schedule Meeting
    meeting_match = re.search(
        r"Schedule a meeting on (\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2}) in (.+)\.",
        q,
        re.IGNORECASE
    )
    if meeting_match:
        date = meeting_match.group(1)
        time = meeting_match.group(2)
        room = meeting_match.group(3)

        return {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": date,
                "time": time,
                "meeting_room": room
            })
        }

    # 3️⃣ Expense Balance
    expense_match = re.search(r"employee\s+(\d+)", q, re.IGNORECASE)
    if "expense balance" in q.lower() and expense_match:
        employee_id = int(expense_match.group(1))
        return {
            "name": "get_expense_balance",
            "arguments": json.dumps({"employee_id": employee_id})
        }

    # 4️⃣ Performance Bonus
    bonus_match = re.search(
        r"employee\s+(\d+).*?(\d{4})",
        q,
        re.IGNORECASE
    )
    if "performance bonus" in q.lower() and bonus_match:
        employee_id = int(bonus_match.group(1))
        year = int(bonus_match.group(2))
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": employee_id,
                "current_year": year
            })
        }

    # 5️⃣ Office Issue (Flexible)
    issue_match = re.search(r"issue\s+(\d+)", q, re.IGNORECASE)
    dept_match = re.search(r"(HR|IT|Facilities|Admin|Finance)", q, re.IGNORECASE)

    if issue_match and dept_match:
        return {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": int(issue_match.group(1)),
                "department": dept_match.group(1)
            })
        }

    from fastapi import HTTPException
    raise HTTPException(status_code=400, detail="Query not recognized")