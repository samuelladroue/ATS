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
    updated_at: Optional[datetime] = None  # Optionnel car peut ne pas exister dans certaines bases

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


class CandidateWithApplications(BaseModel):
    id: UUID
    email: str
    full_name: str
    linkedin_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None  # Optionnel car peut ne pas exister dans certaines bases
    applications: list[ApplicationPublic]

    class Config:
        from_attributes = True


# ===== Application Notes =====

class ApplicationNoteCreate(BaseModel):
    stage: str
    report: str = Field(..., min_length=1)
    rating: int = Field(..., ge=1, le=4)
    interviewer: Optional[str] = None


class ApplicationNote(BaseModel):
    id: int
    application_id: UUID
    stage: str
    report: str
    rating: int
    interviewer: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ===== Email Templates =====

class EmailTemplateCreate(BaseModel):
    name: str = Field(..., min_length=1)
    subject: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)


class EmailTemplateUpdate(BaseModel):
    name: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None


class EmailTemplate(BaseModel):
    id: int
    name: str
    subject: str
    body: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ===== Emails =====

class EmailSend(BaseModel):
    candidate_id: UUID
    subject: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)
    template_id: Optional[int] = None


class Email(BaseModel):
    id: int
    candidate_id: UUID
    subject: str
    body: str
    sender_email: str
    sender_name: Optional[str] = None
    template_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True
