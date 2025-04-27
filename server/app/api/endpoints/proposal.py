from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.proposal import Proposal, ProposalCreate, ProposalUpdate
from app.crud.proposal import (
    get_proposal, get_proposals, create_proposal, update_proposal, delete_proposal
)
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[Proposal])
def read_proposals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_proposals(db, skip=skip, limit=limit)

@router.get("/{proposal_id}", response_model=Proposal)
def read_proposal(proposal_id: str, db: Session = Depends(get_db)):
    db_proposal = get_proposal(db, proposal_id)
    if not db_proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return db_proposal

@router.post("/", response_model=Proposal)
def create_new_proposal(proposal: ProposalCreate, db: Session = Depends(get_db)):
    return create_proposal(db, proposal)

@router.put("/{proposal_id}", response_model=Proposal)
def update_existing_proposal(proposal_id: str, updates: ProposalUpdate, db: Session = Depends(get_db)):
    db_proposal = get_proposal(db, proposal_id)
    if not db_proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return update_proposal(db, db_proposal, updates)

@router.delete("/{proposal_id}")
def delete_existing_proposal(proposal_id: str, db: Session = Depends(get_db)):
    db_proposal = get_proposal(db, proposal_id)
    if not db_proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    delete_proposal(db, db_proposal)
    return {"ok": True}