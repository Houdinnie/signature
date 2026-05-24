import json
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

class MessageAction(str, Enum):
    TASK_ASSIGN = "task_assign"
    TASK_RESULT = "task_result"
    QUERY = "query"
    RESPONSE = "response"
    APPROVAL_REQUEST = "approval_request"
    APPROVAL_RESPONSE = "approval_response"
    STATUS_UPDATE = "status_update"
    ERROR_REPORT = "error_report"
    LOG = "log"
    HEARTBEAT = "heartbeat"
    WORKFLOW_STEP = "workflow_step"
    WORKFLOW_STATUS = "workflow_status"
    MEMORY_STORE = "memory_store"
    MEMORY_RETRIEVE = "memory_retrieve"

class AgentMessage:
    def __init__(self,
                 sender_id: int,
                 receiver_id: int,
                 action: MessageAction,
                 payload: Dict[str, Any] = None,
                 correlation_id: str = None,
                 reply_to: str = None,
                 priority: str = "medium",
                 ttl_seconds: int = 300):
        self.id = str(uuid.uuid4())
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.action = action
        self.payload = payload or {}
        self.correlation_id = correlation_id or str(uuid.uuid4())
        self.reply_to = reply_to
        self.priority = priority
        self.ttl_seconds = ttl_seconds
        self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "action": self.action.value,
            "payload": self.payload,
            "correlation_id": self.correlation_id,
            "reply_to": self.reply_to,
            "priority": self.priority,
            "ttl_seconds": self.ttl_seconds,
            "timestamp": self.timestamp
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentMessage":
        msg = cls(
            sender_id=data["sender_id"],
            receiver_id=data["receiver_id"],
            action=MessageAction(data["action"]),
            payload=data.get("payload", {}),
            correlation_id=data.get("correlation_id"),
            reply_to=data.get("reply_to"),
            priority=data.get("priority", "medium"),
            ttl_seconds=data.get("ttl_seconds", 300)
        )
        msg.id = data.get("id", msg.id)
        msg.timestamp = data.get("timestamp", msg.timestamp)
        return msg

    @classmethod
    def from_json(cls, json_str: str) -> "AgentMessage":
        return cls.from_dict(json.loads(json_str))

    def create_reply(self, payload: Dict[str, Any], action: MessageAction = None) -> "AgentMessage":
        return AgentMessage(
            sender_id=self.receiver_id,
            receiver_id=self.sender_id,
            action=action or MessageAction.RESPONSE,
            payload=payload,
            correlation_id=self.correlation_id,
            reply_to=self.id,
            priority=self.priority,
            ttl_seconds=self.ttl_seconds
        )

    def is_expired(self) -> bool:
        created = datetime.fromisoformat(self.timestamp)
        elapsed = (datetime.utcnow() - created).total_seconds()
        return elapsed > self.ttl_seconds

class TaskPayload:
    @staticmethod
    def create_task(task_type: str, params: Dict[str, Any], metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        return {
            "task_type": task_type,
            "params": params,
            "metadata": metadata or {},
            "assigned_at": datetime.utcnow().isoformat()
        }

    @staticmethod
    def create_result(task_type: str, status: str, data: Dict[str, Any],
                      error: str = None, metrics: Dict[str, Any] = None) -> Dict[str, Any]:
        return {
            "task_type": task_type,
            "status": status,
            "data": data,
            "error": error,
            "metrics": metrics or {},
            "completed_at": datetime.utcnow().isoformat()
        }

    @staticmethod
    def create_approval_request(step_name: str, workflow_name: str,
                                context: Dict[str, Any],
                                risk_level: str) -> Dict[str, Any]:
        return {
            "step_name": step_name,
            "workflow_name": workflow_name,
            "context": context,
            "risk_level": risk_level,
            "requested_at": datetime.utcnow().isoformat()
        }

    @staticmethod
    def create_memory_payload(action: str, memory_type: str,
                              key: str, value: Any,
                              tags: List[str] = None,
                              importance: float = 0.5) -> Dict[str, Any]:
        return {
            "action": action,
            "memory_type": memory_type,
            "key": key,
            "value": value,
            "tags": tags or [],
            "importance": importance,
            "timestamp": datetime.utcnow().isoformat()
        }
