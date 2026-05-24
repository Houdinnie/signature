from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from ...core.database import get_db
from ...services.memory_service import MemoryService
from ...models.memory import MemoryType, MemorySource

router = APIRouter()

@router.post("/store")
async def store_memory(
    agent_id: int,
    key: str,
    value: Any,
    memory_type: str = "semantic",
    source: str = "agent_run",
    summary: str = None,
    tags: str = None,
    importance: float = 0.5,
    db: Session = Depends(get_db)
):
    service = MemoryService(db)
    try:
        mt = MemoryType(memory_type)
        ms = MemorySource(source)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid memory_type or source")
    tag_list = tags.split(",") if tags else None
    entry = service.store(
        agent_id=agent_id,
        memory_type=mt,
        key=key,
        value=value,
        source=ms,
        summary=summary,
        tags=tag_list,
        importance=importance
    )
    return {
        "id": entry.id,
        "key": entry.key,
        "memory_type": entry.memory_type.value,
        "importance": entry.importance_score,
        "created_at": entry.created_at.isoformat() if entry.created_at else None
    }

@router.get("/retrieve")
async def retrieve_memory(
    key: str,
    agent_id: int = None,
    memory_type: str = None,
    db: Session = Depends(get_db)
):
    service = MemoryService(db)
    mt = MemoryType(memory_type) if memory_type else None
    entry = service.retrieve(key, agent_id=agent_id, memory_type=mt)
    if not entry:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {
        "id": entry.id,
        "agent_id": entry.agent_id,
        "key": entry.key,
        "value": entry.value,
        "memory_type": entry.memory_type.value,
        "importance": entry.importance_score,
        "access_count": entry.access_count,
        "created_at": entry.created_at.isoformat() if entry.created_at else None,
        "updated_at": entry.updated_at.isoformat() if entry.updated_at else None
    }

@router.get("/search")
async def search_memory(
    q: str = Query(..., description="Search query"),
    agent_id: int = None,
    memory_type: str = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    service = MemoryService(db)
    mt = MemoryType(memory_type) if memory_type else None
    entries = service.search(q, agent_id=agent_id, memory_type=mt, limit=limit)
    return [
        {
            "id": e.id,
            "key": e.key,
            "summary": e.summary,
            "memory_type": e.memory_type.value,
            "importance": e.importance_score,
            "created_at": e.created_at.isoformat() if e.created_at else None
        }
        for e in entries
    ]

@router.get("/semantic-search")
async def semantic_search(
    q: str = Query(..., description="Semantic search query"),
    agent_id: int = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    service = MemoryService(db)
    results = service.semantic_search(q, agent_id=agent_id, limit=limit)
    return {"results": results, "search_type": "semantic"}

@router.get("/recent")
async def recent_memories(
    agent_id: int = None,
    memory_type: str = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    service = MemoryService(db)
    mt = MemoryType(memory_type) if memory_type else None
    entries = service.get_recent(agent_id=agent_id, memory_type=mt, limit=limit)
    return [
        {
            "id": e.id,
            "key": e.key,
            "summary": e.summary[:100] if e.summary else "",
            "memory_type": e.memory_type.value,
            "importance": e.importance_score,
            "created_at": e.created_at.isoformat() if e.created_at else None
        }
        for e in entries
    ]

@router.get("/important")
async def important_memories(
    agent_id: int = None,
    min_importance: float = 0.7,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    service = MemoryService(db)
    entries = service.get_important(agent_id=agent_id, min_importance=min_importance, limit=limit)
    return [
        {
            "id": e.id,
            "key": e.key,
            "summary": e.summary,
            "importance": e.importance_score,
            "memory_type": e.memory_type.value,
            "created_at": e.created_at.isoformat() if e.created_at else None
        }
        for e in entries
    ]

@router.get("/learning/{agent_id}")
async def get_learnings(
    agent_id: int,
    min_rating: float = 0.0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    service = MemoryService(db)
    learnings = service.get_learnings(agent_id=agent_id, min_rating=min_rating, limit=limit)
    return [
        {
            "id": l.id,
            "trigger_event": l.trigger_event,
            "pattern_detected": l.pattern_detected,
            "action_taken": l.action_taken,
            "outcome": l.outcome,
            "success_rating": l.success_rating,
            "created_at": l.created_at.isoformat() if l.created_at else None
        }
        for l in learnings
    ]

@router.delete("/{memory_id}")
async def delete_memory(memory_id: int, db: Session = Depends(get_db)):
    service = MemoryService(db)
    if service.delete(memory_id):
        return {"status": "deleted", "memory_id": memory_id}
    raise HTTPException(status_code=404, detail="Memory not found")
