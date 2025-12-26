from app.models import Expense, ExpenseApproval, User
from app.schemas import ExpenseCreate
from sqlalchemy.orm import Session
from datetime import datetime
from app.constants import PENDING, APPROVED, REJECTED, ADMIN
from passlib.context import CryptContext

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

def get_user_expenses(db: Session, user_id: int):
    return (
        db.query(Expense)
        .filter(Expense.employee_id == user_id)
        .order_by(Expense.date.desc())
        .all()
    )

def get_expense_details(db:Session, expense_id:int):
    expense_data = db.query(Expense).filter(Expense.id==expense_id).first()
    if not expense_data:
        raise Exception("Expense not found")
    approvals = expense_data.approvals

    return{
        "expense" : expense_data,
        "approvals": approvals
    }


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, email: str, password: str):
    """
    Fetch user by email,
    verify password,
    return user if valid else None.
    """

    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user