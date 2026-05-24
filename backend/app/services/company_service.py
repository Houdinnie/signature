"""Company context — provides full business context for agent prompts."""
import json
import logging
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from ..models.company import CompanyConfig

logger = logging.getLogger(__name__)


def get_company_config(db: Session) -> Optional[CompanyConfig]:
    return db.query(CompanyConfig).first()


def get_full_context(db: Session) -> Dict[str, Any]:
    """Build the full context dict for agent prompts."""
    config = get_company_config(db)
    if not config:
        return {}

    return {
        "company": {
            "name": config.name,
            "mission": config.mission,
            "vision": config.vision,
            "description": config.description,
            "target_market": config.target_market,
            "value_prop": config.value_prop,
            "website_url": config.website_url,
            "github_repo": config.github_repo,
            "product_type": config.product_type,
            "industry": config.industry,
            "timezone": config.timezone,
        },
        "goals": _safe_json(config.goals),
        "kpis": _safe_json(config.kpis),
    }


def _safe_json(value: Optional[str]) -> Any:
    if not value:
        return {}
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return {}
