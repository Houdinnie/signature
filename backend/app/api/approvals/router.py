from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ...core.database import get_db
from ...services.approval_service import ApprovalService
from ...models.workflow import ApprovalRequest, ApprovalStatus, ApprovalLevel

router = APIRouter()

@router.get("/")
async def list_pending_approvals(db: Session = Depends(get_db)):
    service = ApprovalService(db)
    approvals = service.get_pending_approvals()
    return [
        {
            "id": a.id,
            "title": a.title,
            "description": a.description,
            "level": a.level.value if a.level else "human",
            "status": a.status.value,
            "created_at": a.created_at.isoformat() if a.created_at else None
        }
        for a in approvals
    ]

@router.get("/{approval_id}")
async def get_approval(approval_id: int, db: Session = Depends(get_db)):
    service = ApprovalService(db)
    approval = service.get_approval_by_id(approval_id)
    if not approval:
        raise HTTPException(status_code=404, detail="Approval request not found")
    return {
        "id": approval.id,
        "title": approval.title,
        "description": approval.description,
        "level": approval.level.value if approval.level else "human",
        "status": approval.status.value,
        "requested_by": approval.requested_by,
        "approved_by": approval.approved_by,
        "response_message": approval.response_message,
        "created_at": approval.created_at.isoformat() if approval.created_at else None,
        "responded_at": approval.responded_at.isoformat() if approval.responded_at else None
    }

@router.post("/{approval_id}/approve")
async def approve_request(approval_id: int, user_id: int, message: str = None, db: Session = Depends(get_db)):
    service = ApprovalService(db)
    approval = service.approve(approval_id, user_id, message)
    if not approval:
        raise HTTPException(status_code=404, detail="Approval request not found")
    return {"status": "approved", "approval_id": approval_id}

@router.post("/{approval_id}/reject")
async def reject_request(approval_id: int, user_id: int, reason: str, db: Session = Depends(get_db)):
    service = ApprovalService(db)
    approval = service.reject(approval_id, user_id, reason)
    if not approval:
        raise HTTPException(status_code=404, detail="Approval request not found")
    return {"status": "rejected", "approval_id": approval_id, "reason": reason}

@router.get("/stats")
async def approval_stats(db: Session = Depends(get_db)):
    service = ApprovalService(db)
    return service.get_approval_stats()
