# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import auth, attendance, companies, users
from app.core.config import settings

from app.db.init_db import create_first_superuser

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="WorkCheck: A robust employee attendance system with QR code and NFC capabilities",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set up CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["authentication"])
app.include_router(users.router, prefix=settings.API_V1_STR, tags=["users"])
app.include_router(companies.router, prefix=settings.API_V1_STR, tags=["companies"])
app.include_router(attendance.router, prefix=settings.API_V1_STR, tags=["attendance"])

@app.on_event("startup")
async def startup_event():
    await create_first_superuser()


@app.get("/")
def read_root():
    return {"message": "Welcome to WorkCheck Attendance System"}
