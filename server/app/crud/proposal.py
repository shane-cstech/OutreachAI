from sqlalchemy.orm import Session
from app.models.proposal import Proposal
from app.schemas.proposal import ProposalCreate, ProposalUpdate
from typing import List, Optional
import uuid

def get_proposal(db: Session, proposal_id: uuid.UUID) -> Optional[Proposal]:
    return db.query(Proposal).filter(Proposal.id == proposal_id).first()

def get_proposals(db: Session, skip: int = 0, limit: int = 100) -> List[Proposal]:
    return db.query(Proposal).offset(skip).limit(limit).all()

def create_proposal(db: Session, proposal: ProposalCreate) -> Proposal:
    db_proposal = Proposal(**proposal.dict())
    db.add(db_proposal)
    db.commit()
    db.refresh(db_proposal)
    return db_proposal

def update_proposal(db: Session, db_proposal: Proposal, updates: ProposalUpdate) -> Proposal:
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(db_proposal, field, value)
    db.commit()
    db.refresh(db_proposal)
    return db_proposal

def delete_proposal(db: Session, db_proposal: Proposal):
    db.delete(db_proposal)
    db.commit()