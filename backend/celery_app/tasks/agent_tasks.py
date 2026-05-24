"""Per-agent Celery tasks — dispatched by orchestrator or Beat."""
import asyncio
import time
import logging
from celery_app.worker import app

logger = logging.getLogger(__name__)


@app.task(name="celery_app.tasks.agent_tasks.run_agent_task", bind=True, max_retries=2)
def run_agent_task(self, task_id: int):
    async def _execute():
        from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
        from app.core.config import settings
        from app.agents.crew_factory import run_agent_for_task
        from app.services.task_service import get_task, update_task_status, create_agent_run, finish_agent_run
        from app.services.company_service import get_full_context
        from app.services.activity_service import log_activity

        engine = create_async_engine(settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"))
        Session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async with Session() as db:
            task = await get_task(db, task_id)
            if not task:
                return

            await update_task_status(db, task_id, "in_progress")
            context = await get_full_context(db)
            run = await create_agent_run(db, task.agent_type, task_id=task_id, input_context=context)
            await db.commit()

        start = time.monotonic()
        try:
            task_dict = {"id": task.id, "title": task.title, "description": task.description}
            result = run_agent_for_task(task.agent_type, task_dict, context)
            status = "completed"
            summary = result.get("summary", "Task completed.")
            error = None
        except Exception as exc:
            status = "failed"
            summary = None
            error = str(exc)
            result = {}

        duration = round(time.monotonic() - start, 2)

        async with Session() as db:
            await update_task_status(db, task_id, status, result_summary=summary, error_message=error)
            await finish_agent_run(db, run.id, status, output=result, duration_secs=duration)
            await log_activity(
                db,
                agent_type=task.agent_type,
                action="task_completed" if status == "completed" else "task_failed",
                summary=summary or error or "No output",
                level="success" if status == "completed" else "error",
            )
            await db.commit()

        await engine.dispose()

    asyncio.run(_execute())


def _create_and_run(agent_type: str, title: str):
    async def _inner():
        from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
        from app.core.config import settings
        from app.services.task_service import create_task

        engine = create_async_engine(settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"))
        Session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async with Session() as db:
            task = await create_task(db, title=title, agent_type=agent_type, source="scheduler")
            await db.commit()
            task_id = task.id

        await engine.dispose()
        return task_id

    task_id = asyncio.run(_inner())
    run_agent_task.delay(task_id)


@app.task(name="celery_app.tasks.agent_tasks.run_social_sweep")
def run_social_sweep():
    _create_and_run("social_posts", "Check social mentions and reply to engaging comments")


@app.task(name="celery_app.tasks.agent_tasks.run_email_sweep")
def run_email_sweep():
    _create_and_run("support_reply", "Check inbox and reply to customer emails")


@app.task(name="celery_app.tasks.agent_tasks.run_finance_sync")
def run_finance_sync():
    _create_and_run("finance", "Sync revenue data and check for anomalies")
