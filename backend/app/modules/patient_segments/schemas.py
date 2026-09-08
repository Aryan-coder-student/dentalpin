"""Schemas for patient_segments."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SegmentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=60)
    color: str | None = Field(default=None, max_length=7)
    description: str | None = None


class SegmentUpdate(BaseModel):
    """All-optional: PATCH semantics with exclude_unset (M4)."""

    name: str | None = Field(default=None, min_length=1, max_length=60)
    color: str | None = Field(default=None, max_length=7)
    description: str | None = None


class SegmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    color: str | None
    description: str | None
    member_count: int = 0
    created_at: datetime


class SegmentAssign(BaseModel):
    segment_id: UUID


class SegmentMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    patient_id: UUID
    full_name: str
