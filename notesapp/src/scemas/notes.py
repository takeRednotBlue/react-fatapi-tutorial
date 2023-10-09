from datetime import datetime

from pydantic import BaseModel


class NoteBase(BaseModel):
    body: str


class NoteResponse(NoteBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes: bool = True
