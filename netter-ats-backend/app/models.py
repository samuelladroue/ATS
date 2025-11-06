from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


# ===== Jobs =====

class JobCreate(BaseModel):
    slug: str = Field(..., min_length=1)
    title: str
    description_md: Optional[str] = None
    location: Optional[str] = None
    department: Optional[str] = None
    status: str = "open"  # open | closed


class JobPublic(BaseModel):
    id: UUID
    slug: str
    title: str
    description_md: Optional[str] = None
    location: Optional[str] = None
    department: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class JobList(BaseModel):
    id: UUID
    slug: str
    title: str
    location: Optional[str] = None
    department: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ===== Applications =====

class ApplyPayload(BaseModel):
    full_name: str = Field(..., min_length=2)
    email: EmailStr
    linkedin_url: Optional[str] = None


class ApplicationPublic(BaseModel):
    id: UUID
    job_id: UUID
    candidate_id: UUID
    stage: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ApplicationUpdate(BaseModel):
    stage: Optional[str] = None
    notes: Optional[str] = None


class ApplicationWithCandidate(BaseModel):
    id: UUID
    job_id: UUID
    candidate_id: UUID
    stage: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    candidate_name: str
    candidate_email: str
    candidate_linkedin_url: Optional[str] = None

    class Config:
        from_attributes = True
