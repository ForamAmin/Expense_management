from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    ForeignKey,
    Boolean
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db import Base
from app.constants import (
    ADMIN,
    MANAGER,
    EMPLOYEE,
    PENDING,
    APPROVED,
    REJECTED
)
class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    base_currency = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    users = relationship("User", back_populates="company")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    role = Column(String, nullable=False)  # ADMIN / MANAGER / EMPLOYEE

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    company = relationship("Company", back_populates="users")

    manager = relationship(
        "User",
        remote_side=[id],
        backref="subordinates"
    )

    expenses = relationship("Expense", back_populates="employee")
    approvals = relationship("ExpenseApproval", back_populates="approver")

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)
    date = Column(Date, nullable=False)

    status = Column(String, default=PENDING, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    employee = relationship("User", back_populates="expenses")
    approvals = relationship(
        "ExpenseApproval",
        back_populates="expense",
        cascade="all, delete-orphan"
    )

class ExpenseApproval(Base):
    __tablename__ = "expense_approvals"

    id = Column(Integer, primary_key=True, index=True)

    expense_id = Column(Integer, ForeignKey("expenses.id"), nullable=False)
    approver_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    level = Column(Integer, nullable=False)  # 1 = manager, 2 = admin

    status = Column(String, default=PENDING, nullable=False)
    comment = Column(String, nullable=True)

    approved_at = Column(DateTime, nullable=True)

    # Relationships
    expense = relationship("Expense", back_populates="approvals")
    approver = relationship("User", back_populates="approvals")
