# app/main.py
from fastapi import FastAPI
from app.routes import contacts
from app.auth import router as auth_router

app = FastAPI(title="FastAPI Xero Integration")

# Include the authentication endpoints under /auth
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# Include Xero contact endpoints under /api
app.include_router(contacts.router, prefix="/api", tags=["Xero Contacts"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
