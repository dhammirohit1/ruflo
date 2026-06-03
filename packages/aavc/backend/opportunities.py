import json
import logging
from typing import List, Dict, Any
from anthropic import Anthropic
import os

logger = logging.getLogger(__name__)

class OpportunityEngine:
    """Discover, evaluate, and score business opportunities"""
    
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
        self.model = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
    
    def discover_opportunities(self, categories: List[str] = None) -> List[Dict[str, Any]]:
        """Discover new revenue opportunities"""
        if categories is None:
            categories = [
                "SaaS", "Affiliate Marketing", "E-commerce", "Lead Generation",
                "Freelance Services", "Content Monetization", "Digital Products",
                "Marketplace Arbitrage"
            ]
        
        prompt = f"""As a business opportunity scout, identify 8 high-potential online revenue opportunities.
        
Consider these categories: {', '.join(categories)}

For each opportunity, evaluate and return JSON array with:
- title: Brief name
- description: What the business does
- opportunity_type: Category
- entry_cost: Estimated startup cost in USD
- revenue_potential: Estimated monthly revenue range
- competition_level: low/medium/high
- time_to_first_revenue_days: Days before first income
- automation_potential: Degree of automation possible (0-100)
- scalability: Can it grow 10x? (yes/no)
- key_challenges: Main obstacles
- required_skills: What skills needed
- market_score: Market viability (0-100)
- revenue_score: Revenue potential (0-100)
- risk_score: Execution risk (0-100)"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        try:
            text = response.content[0].text
            # Extract JSON from response
            start_idx = text.find('[')
            end_idx = text.rfind(']') + 1
            if start_idx >= 0 and end_idx > start_idx:
                opportunities = json.loads(text[start_idx:end_idx])
                return opportunities
        except json.JSONDecodeError:
            logger.error("Failed to parse opportunities JSON")
            return []
    
    def evaluate_opportunity(self, opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """Deep evaluation of a specific opportunity"""
        prompt = f"""Deeply evaluate this business opportunity:

{json.dumps(opportunity, indent=2)}

Provide:
- Market analysis
- Revenue model details
- Scaling strategy
- Competitive advantages
- Risk mitigation
- 90-day action plan
- Estimated breakeven timeline

Return as structured JSON."""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {
            "opportunity": opportunity['title'],
            "evaluation": response.content[0].text
        }
    
    def validate_opportunity(self, opportunity: Dict[str, Any]) -> bool:
        """Quick validation - is this worth pursuing?"""
        market_score = opportunity.get('market_score', 0)
        revenue_score = opportunity.get('revenue_score', 0)
        risk_score = opportunity.get('risk_score', 100)
        
        # Simple scoring
        if market_score >= 60 and revenue_score >= 60 and risk_score <= 70:
            return True
        return False

class BusinessLauncher:
    """Autonomous business launcher"""
    
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
        self.model = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
    
    def generate_landing_page(self, business_idea: Dict[str, Any]) -> str:
        """Generate HTML for landing page"""
        prompt = f"""Create a compelling HTML landing page for this business:

{json.dumps(business_idea, indent=2)}

Generate professional, conversion-optimized HTML with:
- Hero section with value proposition
- Features/benefits
- Pricing table
- Call-to-action buttons
- Footer with links
- Mobile responsive design

Return ONLY valid HTML code."""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    def create_product_description(self, product_name: str, features: List[str]) -> str:
        """Generate product description for e-commerce"""
        prompt = f"""Write a persuasive product description for:

Product: {product_name}
Features: {', '.join(features)}

Make it engaging, benefit-focused, and optimized for conversions."""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    def generate_marketing_copy(self, business_type: str, target_audience: str) -> Dict[str, str]:
        """Generate marketing copy for campaigns"""
        prompt = f"""Generate marketing copy for a {business_type} targeting {target_audience}.

Provide JSON with:
- headline: Main headline
- subheading: Supporting text
- body: Main message
- cta: Call-to-action text
- social_post_1: LinkedIn post
- social_post_2: Twitter post
- email_subject: Email subject line
- email_body: Email body"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        try:
            text = response.content[0].text
            start_idx = text.find('{')
            end_idx = text.rfind('}') + 1
            if start_idx >= 0 and end_idx > start_idx:
                return json.loads(text[start_idx:end_idx])
        except json.JSONDecodeError:
            logger.error("Failed to parse marketing copy JSON")
        
        return {}
    
    def create_business_plan(self, business_idea: Dict[str, Any]) -> str:
        """Generate a 90-day business plan"""
        prompt = f"""Create a detailed 90-day business execution plan for:

{json.dumps(business_idea, indent=2)}

Include:
- Week 1-2: Setup and infrastructure
- Week 3-4: MVP/Product launch
- Week 5-8: Marketing and lead generation
- Week 9-12: Optimization and scaling

Be specific with actionable tasks and timelines."""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
