from models import Expense
from schemas import ExpenseCreate
from sqlalchemy.orm import Session

def create_expense(db: Session, data: ExpenseCreate):
    expense_instance = Expense(**data.model_dump())
    db.add(expense_instance)
    db.commit()
    db.refresh(expense_instance)
    return expense_instance

