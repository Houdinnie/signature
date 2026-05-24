"""Morning and evening cycle — triggered by Celery Beat."""
import asyncio
import logging
from celery_app.worker import app

logger = logging.getLogger(__name__)


@app.task(name="celery_app.tasks.daily_cycle.run_morning_cycle")
def run_morning_cycle():
    async def _inner():
        from datetime import date
        from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
        from app.core.config import settings
        from app.services.company_service import get_full_context
        from app.services.task_service import create_task
        from app.services.activity_service import log_activity
        from app.agents.crew_factory import run_agent_for_task

        engine = create_async_engine(settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"))
        Session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async with Session() as db:
            context = await get_full_context(db)

            orch_task = {
                "title": "Morning planning cycle",
                "description": f"Generate today's task plan for {date.today()}",
            }
            result = run_agent_for_task("orchestrator", orch_task, context)

            await log_activity(
                db,
                agent_type="orchestrator",
                action="morning_plan_complete",
                summary=result.get("summary", "Morning plan generated"),
                level="success",
            )
            await db.commit()

        for agent_type, title in [
            ("support_reply", "Morning support sweep"),
            ("social_posts", "Morning social check"),
        ]:
            async with Session() as db:
                t = await create_task(db, title=title, agent_type=agent_type, source="scheduler", priority=2)
                await db.commit()
                from celery_app.tasks.agent_tasks import run_agent_task
                run_agent_task.delay(t.id)

        await engine.dispose()

    asyncio.run(_inner())


@app.task(name="celery_app.tasks.daily_cycle.run_evening_cycle")
def run_evening_cycle():
    async def _inner():
        from datetime import date
        from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
        from app.core.config import settings
        from app.services.company_service import get_full_context
        from app.services.activity_service import log_activity
        from app.agents.crew_factory import run_agent_for_task

        engine = create_async_engine(settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"))
        Session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async with Session() as db:
            context = await get_full_context(db)

            orch_task = {
                "title": "Evening reporting cycle",
                "description": f"Generate evening summary for {date.today()}",
            }
            result = run_agent_for_task("orchestrator", orch_task, context)

            await log_activity(
                db,
                agent_type="orchestrator",
                action="evening_summary_complete",
                summary=result.get("summary", "Evening summary complete"),
                level="success",
            )
            await db.commit()

        await engine.dispose()

    asyncio.run(_inner())
