from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.routes.auth import get_current_user

from app.schemas import (
    ExpenseCreate,
    ExpenseResponse,
    ExpenseSummary
)
from app.constants import EMPLOYEE
from app import logic  # logic.py written by DB girls

router = APIRouter(prefix="/expenses", tags=["Expenses"])


# -------------------------------------------------
# POST /expenses  → Submit a new expense
# -------------------------------------------------
@router.post("/", status_code=status.HTTP_201_CREATED)
def submit_expense(
    payload: ExpenseCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Employee submits a new expense
    """

    # Only employees can submit expenses
    if user.role != EMPLOYEE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employees can submit expenses"
        )

    expense = logic.create_expense(db, user.id, payload)

    return {
        "expense_id": expense.id,
        "status": expense.status
    }


# -------------------------------------------------
# GET /expenses/my  → My expense history
# -------------------------------------------------
@router.get("/my", response_model=list[ExpenseSummary])
def my_expenses(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Employee views their own expense history
    """

    expenses = logic.get_user_expenses(db, user.id)
    return expenses


# -------------------------------------------------
# GET /expenses/{expense_id}  → Expense details
# -------------------------------------------------
@router.get("/{expense_id}")
def expense_details(
    expense_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    View expense details including approval chain
    """

    expense = logic.get_expense_details(db, expense_id)

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    return expense
