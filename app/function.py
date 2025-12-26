from models import Expense, ExpenseApproval, User
from schemas import ExpenseCreate
from SQLAlchemy import Session
from _datetime import datetime
from app.constants import PENDING, APPROVED, REJECTED, ADMIN

def create_expense(db: Session, data: ExpenseCreate):
    expense_instance = Expense(**data.model_dump())
    db.add(expense_instance)
    db.commit()
    db.refresh(expense_instance)
    return expense_instance

def get_pending_approvals(db : Session, user_id : int):
    pending_result = db.query(ExpenseApproval).filter(
        ExpenseApproval.approver_id == user_id,
        ExpenseApproval.status == PENDING
    )

def process_approval(
    db: Session,
    approval_id: int,
    user_id: int,
    decision: str,
    comment: str | None
):
    approval = db.query(ExpenseApproval).get(approval_id)
    if not approval:
        raise Exception("Approval task not found")

    if approval.approver_id != user_id:
        raise Exception("You are not allowed to approve this task")

    approval.status = decision
    approval.comment = comment
    approval.approved_at = datetime.utcnow()

    expense = approval.expense

    if decision == REJECTED:
        expense.status = REJECTED
        db.commit()
        return expense

    if approval.level == 1:
        admin = (
            db.query(User)
            .filter(
                User.company_id == expense.employee.company_id,
                User.role == ADMIN
            )
            .first()
        )

        new_task = ExpenseApproval(
            expense_id=expense.id,
            approver_id=admin.id,
            level=2,
            status=PENDING
        )

        db.add(new_task)
        db.commit()
        return expense

    # Final level approved
    if approval.level == 2:
        expense.status = APPROVED
        db.commit()
        return expense
