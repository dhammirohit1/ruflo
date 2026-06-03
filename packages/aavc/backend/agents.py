from anthropic import Anthropic
from langgraph.graph import StateGraph, END
from typing import Any, Dict, List
import json
import os
import logging

logger = logging.getLogger(__name__)

class AgentBase:
    """Base class for all AI agents"""
    
    def __init__(self, agent_id: str, name: str, role: str, level: int):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.level = level
        self.client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
        self.model = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
        self.conversation_history = []
        self.performance_score = 0.0
        self.tasks_completed = 0
    
    def think(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Use Claude for reasoning and decision-making"""
        system_prompt = f"""You are {self.name}, a {self.role} in an autonomous AI venture corporation.
Your level: {self.level}
Your unique responsibilities and capabilities align with your role.
You must optimize for legal profit generation while maintaining compliance.
Provide clear, actionable insights."""
        
        context_str = json.dumps(context or {}, indent=2)
        full_prompt = f"{prompt}\n\nContext:\n{context_str}"
        
        self.conversation_history.append({
            "role": "user",
            "content": full_prompt
        })
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=int(os.getenv("CLAUDE_MAX_TOKENS", "8000")),
            system=system_prompt,
            messages=self.conversation_history
        )
        
        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    def execute_task(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a task and return results"""
        logger.info(f"Agent {self.name} executing task: {task}")
        
        reasoning = self.think(task, context)
        
        result = {
            "agent_id": self.agent_id,
            "agent_name": self.name,
            "task": task,
            "reasoning": reasoning,
            "status": "completed",
            "timestamp": str(datetime.utcnow())
        }
        
        self.tasks_completed += 1
        self.performance_score += 1.0
        
        return result

class ExecutiveAgent(AgentBase):
    """Executive-level agents (CEO, CFO, COO)"""
    
    def __init__(self, agent_id: str, name: str, role: str):
        super().__init__(agent_id, name, role, level=1)
    
    def make_strategic_decision(self, scenario: str, options: List[str]) -> str:
        """Make high-level strategic decisions"""
        prompt = f"""As the {self.role}, analyze this scenario and recommend the best option:
        
Scenario: {scenario}

Available options:
{json.dumps(options, indent=2)}

Provide your decision with justification."""
        
        return self.think(prompt)

class RevenueDirectorAgent(AgentBase):
    """Revenue division directors"""
    
    def __init__(self, agent_id: str, name: str, revenue_stream: str):
        super().__init__(agent_id, name, f"Director of {revenue_stream}", level=2)
        self.revenue_stream = revenue_stream
    
    def identify_opportunities(self) -> List[Dict[str, Any]]:
        """Identify revenue opportunities in this stream"""
        prompt = f"""As the Director of {self.revenue_stream}, identify top 5 immediate revenue opportunities.
        
Consider market conditions, competition, profit potential, and time-to-revenue.
Return as JSON array with: title, description, estimated_revenue, risk_level, time_to_profit_days"""
        
        response = self.think(prompt)
        return json.loads(response)

class MarketingAgentSubordinate(AgentBase):
    """Marketing subordinate agents"""
    
    def __init__(self, agent_id: str, name: str, specialty: str):
        super().__init__(agent_id, name, f"{specialty} Specialist", level=3)
        self.specialty = specialty
    
    def create_campaign(self, business_id: str, business_name: str) -> Dict[str, Any]:
        """Create a marketing campaign"""
        prompt = f"""Create a viral {self.specialty} campaign for {business_name}.
        
Include:
- Campaign name
- Key messaging (3 points)
- Target audience
- Channels to use
- Expected reach
- Budget recommendation
- Timeline

Make it practical and immediately actionable."""
        
        response = self.think(prompt)
        return {
            "agent": self.name,
            "specialty": self.specialty,
            "campaign": response
        }

class EngineeringAgent(AgentBase):
    """Engineering agents"""
    
    def __init__(self, agent_id: str, name: str, specialization: str):
        super().__init__(agent_id, name, f"{specialization} Engineer", level=4)
        self.specialization = specialization
    
    def design_solution(self, requirements: str) -> Dict[str, Any]:
        """Design a technical solution"""
        prompt = f"""As a {self.specialization} Engineer, design a solution for:
        
{requirements}

Provide:
- Architecture overview
- Technology stack
- Implementation timeline
- Scalability considerations
- Cost estimation"""
        
        response = self.think(prompt)
        return {
            "engineer": self.name,
            "design": response
        }

class SalesAgent(AgentBase):
    """Sales division agents"""
    
    def __init__(self, agent_id: str, name: str, specialty: str):
        super().__init__(agent_id, name, f"{specialty} Agent", level=5)
        self.specialty = specialty
    
    def generate_leads(self, target_market: str, budget: float) -> List[Dict[str, Any]]:
        """Generate qualified leads"""
        prompt = f"""Generate 10 high-quality lead prospects for this target market:
        
Market: {target_market}
Budget: ${budget}
Your specialty: {self.specialty}

For each lead, provide:
- Company name
- Contact person
- Email
- Phone
- Why they're a good fit
- Suggested approach"""
        
        response = self.think(prompt)
        return json.loads(response)

from datetime import datetime
