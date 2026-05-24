import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc, func as sql_func
from ..models.memory import MemoryEntry, LearningEntry, MemoryType, MemorySource
from ..core.database import SessionLocal

logger = logging.getLogger(__name__)

class MemoryService:
    def __init__(self, db: Session):
        self.db = db
        self._chroma_client = None
        self._chroma_collection = None

    def _init_chroma(self):
        if self._chroma_client is None:
            try:
                import chromadb
                self._chroma_client = chromadb.HttpClient(
                    host="localhost",
                    port=8000
                )
                self._chroma_collection = self._chroma_client.get_or_create_collection(
                    name="signature_memory",
                    metadata={"hnsw:space": "cosine"}
                )
                logger.info("ChromaDB client initialized")
            except Exception as e:
                logger.warning(f"ChromaDB not available, using SQL-only storage: {e}")

    def store(self,
              agent_id: int,
              memory_type: MemoryType,
              key: str,
              value: Any,
              source: MemorySource = MemorySource.AGENT_RUN,
              summary: str = None,
              tags: List[str] = None,
              importance: float = 0.5) -> MemoryEntry:
        value_str = json.dumps(value) if not isinstance(value, str) else value
        entry = MemoryEntry(
            agent_id=agent_id,
            memory_type=memory_type,
            source=source,
            key=key,
            value=value_str,
            summary=summary or key,
            tags=json.dumps(tags) if tags else None,
            importance_score=importance
        )
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        self._index_in_chroma(entry)
        logger.info(f"Memory stored: type={memory_type.value}, key={key}, importance={importance}")
        return entry

    def retrieve(self, key: str, agent_id: int = None, memory_type: MemoryType = None) -> Optional[MemoryEntry]:
        query = self.db.query(MemoryEntry).filter(MemoryEntry.key == key)
        if agent_id:
            query = query.filter(MemoryEntry.agent_id == agent_id)
        if memory_type:
            query = query.filter(MemoryEntry.memory_type == memory_type)
        entry = query.order_by(desc(MemoryEntry.updated_at)).first()
        if entry:
            entry.access_count += 1
            self.db.commit()
        return entry

    def search(self, query_text: str, agent_id: int = None, memory_type: MemoryType = None,
               limit: int = 10) -> List[MemoryEntry]:
        query = self.db.query(MemoryEntry)
        if agent_id:
            query = query.filter(MemoryEntry.agent_id == agent_id)
        if memory_type:
            query = query.filter(MemoryEntry.memory_type == memory_type)
        search_filter = f"%{query_text}%"
        query = query.filter(
            (MemoryEntry.key.ilike(search_filter)) |
            (MemoryEntry.value.ilike(search_filter)) |
            (MemoryEntry.summary.ilike(search_filter)) |
            (MemoryEntry.tags.ilike(search_filter))
        )
        return query.order_by(desc(MemoryEntry.importance_score)).limit(limit).all()

    def semantic_search(self, query_text: str, agent_id: int = None, limit: int = 10) -> List[Dict[str, Any]]:
        self._init_chroma()
        if self._chroma_collection:
            try:
                where_filter = {"agent_id": str(agent_id)} if agent_id else None
                results = self._chroma_collection.query(
                    query_texts=[query_text],
                    n_results=limit,
                    where=where_filter
                )
                return [
                    {
                        "id": results["ids"][0][i],
                        "key": results["metadatas"][0][i].get("key"),
                        "summary": results["metadatas"][0][i].get("summary"),
                        "score": results["distances"][0][i],
                        "content": results["documents"][0][i]
                    }
                    for i in range(len(results["ids"][0]))
                ] if results["ids"] else []
            except Exception as e:
                logger.error(f"ChromaDB search failed: {e}")
        return []

    def get_recent(self, agent_id: int = None, memory_type: MemoryType = None,
                   limit: int = 20) -> List[MemoryEntry]:
        query = self.db.query(MemoryEntry)
        if agent_id:
            query = query.filter(MemoryEntry.agent_id == agent_id)
        if memory_type:
            query = query.filter(MemoryEntry.memory_type == memory_type)
        return query.order_by(desc(MemoryEntry.created_at)).limit(limit).all()

    def get_important(self, agent_id: int = None, min_importance: float = 0.7,
                      limit: int = 20) -> List[MemoryEntry]:
        query = self.db.query(MemoryEntry).filter(
            MemoryEntry.importance_score >= min_importance
        )
        if agent_id:
            query = query.filter(MemoryEntry.agent_id == agent_id)
        return query.order_by(desc(MemoryEntry.importance_score)).limit(limit).all()

    def delete(self, memory_id: int) -> bool:
        entry = self.db.query(MemoryEntry).filter(MemoryEntry.id == memory_id).first()
        if entry:
            self.db.delete(entry)
            self.db.commit()
            return True
        return False

    def record_learning(self,
                        agent_id: int,
                        trigger_event: str,
                        pattern_detected: str,
                        action_taken: str = None,
                        outcome: str = None,
                        success_rating: float = 0.5,
                        tags: List[str] = None) -> LearningEntry:
        entry = LearningEntry(
            agent_id=agent_id,
            trigger_event=trigger_event,
            pattern_detected=pattern_detected,
            action_taken=action_taken,
            outcome=outcome,
            success_rating=success_rating,
            tags=json.dumps(tags) if tags else None
        )
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        logger.info(f"Learning recorded for agent {agent_id}: {trigger_event}")
        return entry

    def get_learnings(self, agent_id: int = None, min_rating: float = 0.0,
                      limit: int = 20) -> List[LearningEntry]:
        query = self.db.query(LearningEntry).filter(
            LearningEntry.success_rating >= min_rating
        )
        if agent_id:
            query = query.filter(LearningEntry.agent_id == agent_id)
        return query.order_by(desc(LearningEntry.success_rating)).limit(limit).all()

    def get_stats(self, agent_id: int = None) -> Dict[str, Any]:
        query = self.db.query(MemoryEntry)
        if agent_id:
            query = query.filter(MemoryEntry.agent_id == agent_id)
        total = query.count()
        type_counts = {}
        if total > 0:
            for mt in MemoryType:
                count = query.filter(MemoryEntry.memory_type == mt).count()
                if count > 0:
                    type_counts[mt.value] = count
        avg_importance = self.db.query(sql_func.avg(MemoryEntry.importance_score)).scalar() or 0.0
        return {
            "total_entries": total,
            "by_type": type_counts,
            "avg_importance": round(avg_importance, 2),
            "total_learnings": self.db.query(LearningEntry).count()
        }

    def _index_in_chroma(self, entry: MemoryEntry):
        self._init_chroma()
        if self._chroma_collection:
            try:
                self._chroma_collection.add(
                    ids=[str(entry.id)],
                    documents=[entry.value[:5000]],
                    metadatas=[{
                        "key": entry.key,
                        "summary": entry.summary or "",
                        "agent_id": str(entry.agent_id) if entry.agent_id else "",
                        "memory_type": entry.memory_type.value,
                        "source": entry.source.value,
                        "importance": entry.importance_score
                    }]
                )
            except Exception as e:
                logger.debug(f"Chroma indexing skipped: {e}")

def get_memory_service(db: Session = None) -> MemoryService:
    if db is None:
        db = SessionLocal()
    return MemoryService(db)
