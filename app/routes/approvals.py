from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.routes.auth import get_current_user

from app.schemas import ApprovalAction
from app.constants import MANAGER, ADMIN
from app import logic  # logic.py written by DB girls

router = APIRouter(prefix="/approvals", tags=["Approvals"])


# -------------------------------------------------
# GET /approvals/pending  → My approval to-do list
# -------------------------------------------------
@router.get("/pending")
def get_pending_approvals(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Manager/Admin sees expenses waiting for their approval
    """

    # Only managers/admins can approve
    if user.role not in [MANAGER, ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to approve expenses"
        )

    approvals = logic.get_pending_approvals(db, user.id)
    return approvals


# -------------------------------------------------
# POST /approvals/{approval_id}/action
# -------------------------------------------------
@router.post("/{approval_id}/action")
def approve_or_reject_expense(
    approval_id: int,
    payload: ApprovalAction,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Manager/Admin approves or rejects an expense
    """

    # Only managers/admins can approve
    if user.role not in [MANAGER, ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to approve expenses"
        )

    try:
        result = logic.process_approval(
            db=db,
            approval_id=approval_id,
            user_id=user.id,
            decision=payload.decision,
            comment=payload.comment
        )
    except ValueError as e:
        # Logic layer raises ValueError for invalid actions
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return result
