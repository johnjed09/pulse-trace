from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field


class VisitLogBase(SQLModel):
    path: str = Field(index=True, description="Visited route")
    visitor_id: str = Field(index=True, description="Unique visitor identifier")
    referrer: Optional[str] = Field(
        default=None, description="URL where user came from"
    )
    user_agent: str = Field(description="Client or device information")
    ip_address: Optional[str] = Field(default=None, description="Client IP address")


class VisitLog(VisitLogBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ip_address: Optional[str] = Field(default=None, description="Client IP address")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        index=True,
        description="Timestamp of the visit",
    )


class VisitLogCreate(VisitLogBase):
    pass
