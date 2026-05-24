from fastapi import APIRouter

api_router = APIRouter()

from ..auth.router import router as auth_router
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])

from ..agents.router import router as agents_router
api_router.include_router(agents_router, prefix="/agents", tags=["agents"])

from ..tasks.router import router as tasks_router
api_router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])

from ..dashboard.router import router as dashboard_router
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])

from ..approvals.router import router as approvals_router
api_router.include_router(approvals_router, prefix="/approvals", tags=["approvals"])

from ..messaging.router import router as messaging_router
api_router.include_router(messaging_router, prefix="/messages", tags=["messages"])

from ..memory.router import router as memory_router
api_router.include_router(memory_router, prefix="/memory", tags=["memory"])

from ..workflows.router import router as workflows_router
api_router.include_router(workflows_router, prefix="/workflows", tags=["workflows"])
