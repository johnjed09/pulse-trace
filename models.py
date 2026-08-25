from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class VisitLogBase(SQLModel):
    path: str = Field(index=True, description="Visited route")
    referrer: Optional[str] = Field(
        default=None, description="URL where user came from"
    )
    user_agent: str = Field(description="Client or device information")
    ip_address: Optional[str] = Field(default=None, description="Client IP address")


class VisitLog(VisitLogBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        index=True,
        description="Timestamp of the visit",
    )


class VisitLogCreate(VisitLogBase):
    pass
