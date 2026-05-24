import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from ..models.workflow import ApprovalRequest, ApprovalStatus, ApprovalLevel, WorkflowInstance, WorkflowStep
from ..core.database import SessionLocal

logger = logging.getLogger(__name__)

class ApprovalService:
    def __init__(self, db: Session):
        self.db = db

    def create_approval_request(self,
                                title: str,
                                description: str,
                                level: ApprovalLevel = ApprovalLevel.HUMAN,
                                workflow_id: int = None,
                                step_id: int = None,
                                requested_by: int = None,
                                context: Dict[str, Any] = None) -> ApprovalRequest:
        request = ApprovalRequest(
            workflow_id=workflow_id,
            step_id=step_id,
            title=title,
            description=description,
            level=level,
            status=ApprovalStatus.PENDING,
            requested_by=requested_by,
            context_json=json.dumps(context) if context else None
        )
        self.db.add(request)
        self.db.commit()
        self.db.refresh(request)
        logger.info(f"Approval request created: {request.id} - {title}")
        return request

    def approve(self, request_id: int, approved_by: int, message: str = None) -> Optional[ApprovalRequest]:
        request = self.db.query(ApprovalRequest).filter(ApprovalRequest.id == request_id).first()
        if not request:
            return None
        request.status = ApprovalStatus.APPROVED
        request.approved_by = approved_by
        request.response_message = message
        request.responded_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(request)
        logger.info(f"Approval request {request_id} approved by user {approved_by}")
        return request

    def reject(self, request_id: int, rejected_by: int, reason: str) -> Optional[ApprovalRequest]:
        request = self.db.query(ApprovalRequest).filter(ApprovalRequest.id == request_id).first()
        if not request:
            return None
        request.status = ApprovalStatus.REJECTED
        request.approved_by = rejected_by
        request.response_message = reason
        request.responded_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(request)
        logger.info(f"Approval request {request_id} rejected by user {rejected_by}: {reason}")
        return request

    def get_pending_approvals(self, user_id: int = None) -> List[ApprovalRequest]:
        query = self.db.query(ApprovalRequest).filter(
            ApprovalRequest.status == ApprovalStatus.PENDING
        )
        return query.all()

    def get_approval_by_id(self, request_id: int) -> Optional[ApprovalRequest]:
        return self.db.query(ApprovalRequest).filter(ApprovalRequest.id == request_id).first()

    def get_approvals_for_workflow(self, workflow_id: int) -> List[ApprovalRequest]:
        return self.db.query(ApprovalRequest).filter(
            ApprovalRequest.workflow_id == workflow_id
        ).all()

    def evaluate_auto_approval(self, step: WorkflowStep, context: Dict[str, Any]) -> bool:
        risk_assessment = self._assess_risk(step, context)
        if risk_assessment["score"] < 0.3:
            return True
        return False

    def _assess_risk(self, step: WorkflowStep, context: Dict[str, Any]) -> Dict[str, float]:
        score = 0.0
        risk_levels = {"low": 0.1, "medium": 0.5, "high": 0.9}
        score += risk_levels.get(step.risk_level, 0.1)
        if context.get("involves_production", False):
            score += 0.3
        if context.get("involves_customer_data", False):
            score += 0.2
        if context.get("involves_financial_transaction", False):
            score += 0.3
        if context.get("is_reversible", True):
            score -= 0.1
        return {"score": min(score, 1.0), "level": step.risk_level}

    def get_approval_stats(self) -> Dict[str, Any]:
        total = self.db.query(ApprovalRequest).count()
        pending = self.db.query(ApprovalRequest).filter(
            ApprovalRequest.status == ApprovalStatus.PENDING
        ).count()
        approved = self.db.query(ApprovalRequest).filter(
            ApprovalRequest.status == ApprovalStatus.APPROVED
        ).count()
        rejected = self.db.query(ApprovalRequest).filter(
            ApprovalRequest.status == ApprovalStatus.REJECTED
        ).count()
        return {
            "total": total,
            "pending": pending,
            "approved": approved,
            "rejected": rejected,
            "approval_rate": (approved / total * 100) if total > 0 else 0
        }

def get_approval_service(db: Session = None) -> ApprovalService:
    if db is None:
        db = SessionLocal()
    return ApprovalService(db)
