from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import Note
from src.schemas.notes import NoteBase, NoteResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
def getRoutes():
    return ['/notes', '/notes/<ID>']


@app.get("/notes", response_model=list[NoteResponse])
async def getNotes(db: db_dependency):
    statement = select(Note).order_by(desc(Note.updated_at))
    notes = await db.execute(statement).scalars()
    return notes

@app.get("/notes/{id}", response_model=NoteResponse)
def getNote(id: str, db: db_dependency):
    statement = select(Note).filter(Note.id == id)
    note = db.execute(statement).scalar_one_or_none()
    return note

@app.post("/notes", response_model=list[NoteResponse])
def addNotes(db: db_dependency, body: NoteBase):
    note = Note(**body.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return db.execute(select(Note)).scalars()


@app.put("/notes/{id}", response_model=list[NoteResponse])
def updateNote(id: str, data: NoteBase, db: db_dependency):
    statement = select(Note).filter(Note.id == id)
    note = db.execute(statement).scalar_one_or_none()
    if note:
        note.body = data.body
        note.updated_at = datetime.now()
    db.commit()
    db.refresh(note)
    return db.execute(select(Note)).scalars()


@app.delete("/notes/{id}", response_model=list[NoteResponse])
def deleteNote(id: str, db: db_dependency):
    statement = select(Note).filter(Note.id == id)
    contact = db.execute(statement).scalar_one_or_none()
    if not contact:
        return None
    db.delete(contact)
    db.commit()
    return db.execute(select(Note)).scalars()
