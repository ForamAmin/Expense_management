from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, Field
from app.constants import ADMIN, MANAGER, EMPLOYEE
from app.constants import PENDING, APPROVED, REJECTED

#Company Schema used when creating and responding company data 
class CompanyBase(BaseModel):
    name: str
    base_currency: str

#This is what frontend must send when creating a company.
class CompanyCreate(CompanyBase):
    pass

#This is what backend sends when responding with company data.
class CompanyResponse(CompanyBase):
    id: int
    created_at: datetime


#User Schema , common user fields irrespective of create or response
class UserBase(BaseModel):
    name: str
    email: str
    role: str = Field(..., example=EMPLOYEE)
    company_id: int
    manager_id: Optional[int] = None

#This is what frontend must send when creating a user.
class UserCreate(UserBase):
    password: str

#This is what backend sends when responding with user data.
class UserResponse(UserBase):
    id: int


#This is what frontend must send when logging in.
#backend saying "“For login, I expect only email and password. Nothing else.”"
class LoginRequest(BaseModel):
    email: str
    password: str

#This is what backend sends when responding to a login request.
#backend saying "“On successful login, I will send user_id, role, and company_id.”"
class LoginResponse(BaseModel):
    user_id: int
    role: str
    company_id: int

#Expense Schema

#This is what frontend must send when creating an expense.
class ExpenseCreate(BaseModel):
    amount: float
    currency: str
    category: str
    description: Optional[str] = None
    date: date

#Expense Response Schema
#this is what backend sends when responding with expense data saying "“When I send expense data, 
# I will include all fields plus id, employee_id, status, and created_at.”"
class ExpenseResponse(BaseModel):
    id: int
    employee_id: int
    amount: float
    currency: str
    category: str
    description: Optional[str]
    date: date
    status: str
    created_at: datetime


#Expense History Schema
#this is what backend sends when responding with expense history data
class ExpenseSummary(BaseModel):
    id: int
    amount: float
    currency: str
    category: str
    status: str
    date: date


#Expense approval Schema
#this is what frontend must send when approving or rejecting an expense.
#i.e approver should not send expense_id, approver_id, status, approved_at, level , only decision and optional comment
class ApprovalAction(BaseModel):
    decision: str = Field(..., example=APPROVED)
    comment: Optional[str] = None

#Approval record Schema
#this is what backend sends when responding with expense approval data
#i.e it includes all fields , who approved what expense at what level and when (transparent to frontend)
class ExpenseApprovalResponse(BaseModel):
    id: int
    expense_id: int
    approver_id: int
    status: str
    comment: Optional[str]
    approved_at: Optional[datetime]
    level: int

    class Config:
        orm_mode = True

#Pending approvals Schema
#this is what backend sends when responding with pending approvals for a manager
#i.e saying "“What do i need to approve? ( manager’s perspective)”"
class PendingApprovalItem(BaseModel):
    approval_id: int
    expense_id: int
    employee_id: int
    amount: float
    currency: str
    category: str
    submitted_at: datetime
    level: int
