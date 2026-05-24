import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from ..models.message import Message, MessageStatus, MessageType, MessagePriority
from ..core.message_protocol import AgentMessage, MessageAction
from ..core.database import SessionLocal

logger = logging.getLogger(__name__)

class MessagingService:
    def __init__(self, db: Session):
        self.db = db
        self._subscriptions: Dict[str, List[int]] = {}

    def send_message(self,
                     sender_id: int,
                     receiver_id: int,
                     message_type: MessageType,
                     body: str = None,
                     subject: str = None,
                     metadata: Dict[str, Any] = None,
                     priority: MessagePriority = MessagePriority.MEDIUM,
                     thread_id: str = None,
                     reply_to_id: int = None) -> Message:
        message = Message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            message_type=message_type,
            priority=priority,
            status=MessageStatus.PENDING,
            subject=subject,
            body=body,
            metadata_json=json.dumps(metadata) if metadata else None,
            thread_id=thread_id,
            reply_to_id=reply_to_id
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        message.status = MessageStatus.DELIVERED
        message.delivered_at = datetime.utcnow()
        self.db.commit()
        logger.info(f"Message {message.id} sent from agent {sender_id} to agent {receiver_id}")
        return message

    def send_agent_message(self, agent_message: AgentMessage) -> Message:
        msg_type_map = {
            MessageAction.TASK_ASSIGN: MessageType.TASK,
            MessageAction.TASK_RESULT: MessageType.RESULT,
            MessageAction.QUERY: MessageType.QUERY,
            MessageAction.RESPONSE: MessageType.RESPONSE,
            MessageAction.APPROVAL_REQUEST: MessageType.APPROVAL_REQUEST,
            MessageAction.APPROVAL_RESPONSE: MessageType.APPROVAL_RESPONSE,
            MessageAction.STATUS_UPDATE: MessageType.LOG,
            MessageAction.ERROR_REPORT: MessageType.LOG,
            MessageAction.LOG: MessageType.LOG,
            MessageAction.HEARTBEAT: MessageType.LOG,
            MessageAction.WORKFLOW_STEP: MessageType.TASK,
            MessageAction.WORKFLOW_STATUS: MessageType.RESULT,
            MessageAction.MEMORY_STORE: MessageType.LOG,
            MessageAction.MEMORY_RETRIEVE: MessageType.QUERY,
        }
        msg_type = msg_type_map.get(agent_message.action, MessageType.LOG)
        priority_map = {
            "low": MessagePriority.LOW,
            "medium": MessagePriority.MEDIUM,
            "high": MessagePriority.HIGH
        }
        priority = priority_map.get(agent_message.priority, MessagePriority.MEDIUM)
        return self.send_message(
            sender_id=agent_message.sender_id,
            receiver_id=agent_message.receiver_id,
            message_type=msg_type,
            body=agent_message.to_json(),
            subject=agent_message.action.value,
            metadata=agent_message.payload,
            priority=priority,
            thread_id=agent_message.correlation_id
        )

    def get_inbox(self, agent_id: int, status: MessageStatus = None, limit: int = 50) -> List[Message]:
        query = self.db.query(Message).filter(Message.receiver_id == agent_id)
        if status:
            query = query.filter(Message.status == status)
        return query.order_by(Message.created_at.desc()).limit(limit).all()

    def get_outbox(self, agent_id: int, limit: int = 50) -> List[Message]:
        return self.db.query(Message).filter(
            Message.sender_id == agent_id
        ).order_by(Message.created_at.desc()).limit(limit).all()

    def mark_as_read(self, message_id: int) -> Optional[Message]:
        message = self.db.query(Message).filter(Message.id == message_id).first()
        if message:
            message.status = MessageStatus.READ
            message.read_at = datetime.utcnow()
            self.db.commit()
        return message

    def get_thread(self, thread_id: str) -> List[Message]:
        return self.db.query(Message).filter(
            Message.thread_id == thread_id
        ).order_by(Message.created_at.asc()).all()

    def get_conversation(self, agent1_id: int, agent2_id: int, limit: int = 100) -> List[Message]:
        return self.db.query(Message).filter(
            ((Message.sender_id == agent1_id) & (Message.receiver_id == agent2_id)) |
            ((Message.sender_id == agent2_id) & (Message.receiver_id == agent1_id))
        ).order_by(Message.created_at.desc()).limit(limit).all()

    def subscribe(self, agent_id: int, message_type: str):
        if message_type not in self._subscriptions:
            self._subscriptions[message_type] = []
        if agent_id not in self._subscriptions[message_type]:
            self._subscriptions[message_type].append(agent_id)
            logger.info(f"Agent {agent_id} subscribed to {message_type} messages")

    def unsubscribe(self, agent_id: int, message_type: str = None):
        if message_type:
            subs = self._subscriptions.get(message_type, [])
            if agent_id in subs:
                subs.remove(agent_id)
        else:
            for msg_type in list(self._subscriptions.keys()):
                subs = self._subscriptions[msg_type]
                if agent_id in subs:
                    subs.remove(agent_id)

    def broadcast(self, message_type: str, payload: Dict[str, Any], sender_id: int = 0):
        subscribers = self._subscriptions.get(message_type, [])
        for agent_id in subscribers:
            if agent_id != sender_id:
                self.send_message(
                    sender_id=sender_id,
                    receiver_id=agent_id,
                    message_type=MessageType.LOG,
                    body=json.dumps(payload),
                    subject=f"broadcast:{message_type}",
                    metadata=payload
                )

    def get_unread_count(self, agent_id: int) -> int:
        return self.db.query(Message).filter(
            Message.receiver_id == agent_id,
            Message.status == MessageStatus.DELIVERED
        ).count()

    def delete_message(self, message_id: int) -> bool:
        message = self.db.query(Message).filter(Message.id == message_id).first()
        if message:
            self.db.delete(message)
            self.db.commit()
            return True
        return False

def get_messaging_service(db: Session = None) -> MessagingService:
    if db is None:
        db = SessionLocal()
    return MessagingService(db)
