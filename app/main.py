from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, expenses, approvals

app = FastAPI(
    title="Expense Management System",
    version="1.0.0"
)

# --------------------
# CORS (for frontend)
# --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# Register Routes
# --------------------
app.include_router(auth.router)
app.include_router(expenses.router)
app.include_router(approvals.router)


# --------------------
# Health Check
# --------------------
@app.get("/")
def root():
    return {"status": "Backend is running"}
