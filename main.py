from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, SQLModel

import models
from database import engine, get_session
from models import VisitLog, VisitLogCreate
from analyzer import get_visit_metrics


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="Pulse Trace Analytics API",
    lifespan=lifespan,
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "https://johnjed09.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/")
def read_root():
    return {"status": "online", "message": "PulseTrace API is running!"}


@app.post("/api/v1/track", status_code=201)
def track_visit(
    log_data: VisitLogCreate, request: Request, db: Session = Depends(get_session)
):
    db_log = VisitLog.model_validate(log_data)

    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        db_log.ip_address = forwarded_for.split(",")[0].strip()
    else:
        db_log.ip_address = request.client.host if request.client else None

    db.add(db_log)
    db.commit()
    db.refresh(db_log)

    return {"status": "recorded", "id": db_log.id}


@app.get("/api/v1/analytics/summary")
def get_analytics():
    """Return aggregated analytics metrics."""
    return get_visit_metrics()
