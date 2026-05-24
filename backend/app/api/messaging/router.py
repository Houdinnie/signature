from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ...core.database import get_db
from ...services.messaging_service import MessagingService
from ...models.message import MessageType, MessagePriority

router = APIRouter()

@router.post("/send")
async def send_message(
    sender_id: int,
    receiver_id: int,
    message_type: str = "task",
    body: str = None,
    subject: str = None,
    priority: str = "medium",
    db: Session = Depends(get_db)
):
    service = MessagingService(db)
    try:
        msg_type = MessageType(message_type)
        msg_priority = MessagePriority(priority)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid message_type or priority")
    message = service.send_message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        message_type=msg_type,
        body=body,
        subject=subject,
        priority=msg_priority
    )
    return {
        "id": message.id,
        "status": "sent",
        "sender_id": sender_id,
        "receiver_id": receiver_id
    }

@router.get("/inbox/{agent_id}")
async def get_inbox(agent_id: int, limit: int = 50, db: Session = Depends(get_db)):
    service = MessagingService(db)
    messages = service.get_inbox(agent_id, limit=limit)
    return [
        {
            "id": m.id,
            "sender_id": m.sender_id,
            "message_type": m.message_type.value,
            "subject": m.subject,
            "priority": m.priority.value,
            "status": m.status.value,
            "created_at": m.created_at.isoformat() if m.created_at else None
        }
        for m in messages
    ]

@router.get("/outbox/{agent_id}")
async def get_outbox(agent_id: int, limit: int = 50, db: Session = Depends(get_db)):
    service = MessagingService(db)
    messages = service.get_outbox(agent_id, limit=limit)
    return [
        {
            "id": m.id,
            "receiver_id": m.receiver_id,
            "message_type": m.message_type.value,
            "subject": m.subject,
            "priority": m.priority.value,
            "status": m.status.value,
            "created_at": m.created_at.isoformat() if m.created_at else None
        }
        for m in messages
    ]

@router.get("/conversation/{agent1_id}/{agent2_id}")
async def get_conversation(agent1_id: int, agent2_id: int, limit: int = 100, db: Session = Depends(get_db)):
    service = MessagingService(db)
    messages = service.get_conversation(agent1_id, agent2_id, limit=limit)
    return [
        {
            "id": m.id,
            "sender_id": m.sender_id,
            "receiver_id": m.receiver_id,
            "message_type": m.message_type.value,
            "subject": m.subject,
            "body": m.body,
            "priority": m.priority.value,
            "status": m.status.value,
            "created_at": m.created_at.isoformat() if m.created_at else None
        }
        for m in messages
    ]

@router.get("/unread/{agent_id}")
async def get_unread_count(agent_id: int, db: Session = Depends(get_db)):
    service = MessagingService(db)
    count = service.get_unread_count(agent_id)
    return {"agent_id": agent_id, "unread_count": count}

@router.post("/{message_id}/read")
async def mark_as_read(message_id: int, db: Session = Depends(get_db)):
    service = MessagingService(db)
    message = service.mark_as_read(message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"status": "read", "message_id": message_id}

@router.delete("/{message_id}")
async def delete_message(message_id: int, db: Session = Depends(get_db)):
    service = MessagingService(db)
    if service.delete_message(message_id):
        return {"status": "deleted", "message_id": message_id}
    raise HTTPException(status_code=404, detail="Message not found")
