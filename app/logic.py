# app/logic.py

from app.models import User, Expense
from app.constants import PENDING

# --------------------
# AUTH
# --------------------
def authenticate_user(db, email, password):
    return db.query(User).filter(User.email == email).first()


# --------------------
# EXPENSES
# --------------------
def create_expense(db, user_id, payload):
    expense = Expense(
        employee_id=user_id,
        amount=payload.amount,
        currency=payload.currency,
        category=payload.category,
        description=payload.description,
        date=payload.date,
        status=PENDING
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def get_user_expenses(db, user_id):
    return db.query(Expense).filter(Expense.employee_id == user_id).all()


def get_expense_details(db, expense_id):
    return {
        "id": expense_id,
        "approvals": []
    }


# --------------------
# APPROVALS
# --------------------
def get_pending_approvals(db, user_id):
    return []


def process_approval(db, approval_id, user_id, decision, comment=None):
    return {
        "status": "success",
        "new_expense_status": "APPROVED"
    }
