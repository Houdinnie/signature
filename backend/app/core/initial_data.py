from sqlalchemy.orm import Session
from ..models.agent import Agent, AgentType
from ..schemas.agent import AgentCreate

def init_agents(db: Session):
    """Initialize default agents"""
    # Check if agents already exist
    existing_agents = db.query(Agent).count()
    if existing_agents > 0:
        return  # Agents already initialized
    
    # Define default agents
    default_agents = [
        {
            "name": "Orchestrator Agent",
            "agent_type": AgentType.ORCHESTRATOR,
            "description": "The central AI coordinator responsible for planning, prioritization, delegation, and summarization"
        },
        {
            "name": "Planning Agent",
            "agent_type": AgentType.PLANNING,
            "description": "Responsible for strategy planning, roadmap creation, OKR generation, and operational prioritization"
        },
        {
            "name": "Competitor Research Agent",
            "agent_type": AgentType.COMPETITOR_RESEARCH,
            "description": "Monitors competitors, tracks pricing changes, product launches, market analysis, and trend detection"
        },
        {
            "name": "Social Posts Agent",
            "agent_type": AgentType.SOCIAL_POSTS,
            "description": "Generates social content, repurposes content, schedules campaigns, and optimizes engagement"
        },
        {
            "name": "Email Outreach Agent",
            "agent_type": AgentType.EMAIL_OUTREACH,
            "description": "Handles lead outreach, follow-up sequences, email personalization, and nurture campaigns"
        },
        {
            "name": "Support Reply Agent",
            "agent_type": AgentType.SUPPORT_REPLY,
            "description": "Summarizes support emails, generates reply drafts, escalates urgent issues, and maintains FAQ memory"
        },
        {
            "name": "Ads Agent",
            "agent_type": AgentType.ADS,
            "description": "Generates campaigns, creates ad copy, analyzes budgets, and tracks ROAS"
        },
        {
            "name": "Code Agent",
            "agent_type": AgentType.CODE,
            "description": "Generates code, modifies repositories, executes CLI tasks, creates pull requests, and automates engineering workflows"
        },
        {
            "name": "Finance Agent",
            "agent_type": AgentType.FINANCE,
            "description": "Tracks PayPal revenue, monitors subscription analytics, processes payments, and provides cashflow summaries"
        }
    ]
    
    # Create agents
    for agent_data in default_agents:
        agent = AgentCreate(**agent_data)
        db_agent = Agent(
            name=agent.name,
            agent_type=agent.agent_type,
            description=agent.description,
            is_active=agent.is_active
        )
        db.add(db_agent)
    
    db.commit()
    print("Initialized default agents")