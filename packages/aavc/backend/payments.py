import stripe
import os
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

# Initialize payment processors
stripe.api_key = os.getenv("STRIPE_API_KEY")

class PaymentProcessor:
    """Handle payment processing and transfers"""
    
    @staticmethod
    async def create_bank_transfer(amount: float, account_id: str, description: str = "") -> Dict[str, Any]:
        """Create bank transfer via Stripe"""
        try:
            transfer = stripe.Transfer.create(
                amount=int(amount * 100),  # Stripe uses cents
                currency="usd",
                destination=account_id,
                description=description
            )
            return {
                "status": "success",
                "transaction_id": transfer.id,
                "amount": amount,
                "type": "bank_transfer"
            }
        except stripe.error.StripeError as e:
            logger.error(f"Bank transfer failed: {str(e)}")
            return {
                "status": "failed",
                "error": str(e),
                "type": "bank_transfer"
            }
    
    @staticmethod
    async def create_paypal_transfer(amount: float, email: str, description: str = "") -> Dict[str, Any]:
        """Create PayPal transfer"""
        # This would integrate with PayPal API
        # For now, returning mock response
        return {
            "status": "pending",
            "transaction_id": f"PP_{int(amount*1000)}",
            "amount": amount,
            "type": "paypal_transfer",
            "note": "PayPal integration requires additional setup"
        }
    
    @staticmethod
    async def create_crypto_transfer(amount: float, wallet_address: str, description: str = "") -> Dict[str, Any]:
        """Create cryptocurrency transfer"""
        # This would integrate with Web3.py or similar
        # For now, returning mock response
        return {
            "status": "pending",
            "transaction_id": f"CRYPTO_{amount}",
            "amount": amount,
            "type": "crypto_transfer",
            "wallet": wallet_address,
            "note": "Crypto transfer requires blockchain integration"
        }

class RevenueTracker:
    """Track revenue from all sources"""
    
    @staticmethod
    def get_revenue_summary(db, days: int = 1) -> Dict[str, Any]:
        """Get revenue summary for last N days"""
        from datetime import datetime, timedelta
        from models import Revenue
        
        start_date = datetime.utcnow() - timedelta(days=days)
        revenues = db.query(Revenue).filter(Revenue.created_at >= start_date).all()
        
        total = sum(r.amount for r in revenues)
        by_source = {}
        for r in revenues:
            by_source[r.source] = by_source.get(r.source, 0) + r.amount
        
        return {
            "total": total,
            "by_source": by_source,
            "count": len(revenues),
            "period_days": days
        }

class ExpenseTracker:
    """Track expenses and costs"""
    
    @staticmethod
    def get_expense_summary(db, days: int = 1) -> Dict[str, Any]:
        """Get expense summary for last N days"""
        from datetime import datetime, timedelta
        from models import Expense
        
        start_date = datetime.utcnow() - timedelta(days=days)
        expenses = db.query(Expense).filter(Expense.created_at >= start_date).all()
        
        total = sum(e.amount for e in expenses)
        by_category = {}
        for e in expenses:
            by_category[e.category] = by_category.get(e.category, 0) + e.amount
        
        return {
            "total": total,
            "by_category": by_category,
            "count": len(expenses),
            "period_days": days
        }

class ProfitCalculator:
    """Calculate profit and ROI"""
    
    @staticmethod
    def calculate_profit(revenue: float, expenses: float) -> float:
        """Calculate net profit"""
        return revenue - expenses
    
    @staticmethod
    def calculate_roi(revenue: float, expenses: float) -> float:
        """Calculate ROI percentage"""
        if expenses == 0:
            return 0.0
        return ((revenue - expenses) / expenses) * 100
    
    @staticmethod
    def get_dashboard_metrics(db) -> Dict[str, Any]:
        """Get comprehensive dashboard metrics"""
        from datetime import datetime, timedelta
        
        # Today
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_revenue = RevenueTracker.get_revenue_summary(db, days=1)
        today_expenses = ExpenseTracker.get_expense_summary(db, days=1)
        
        # Week
        week_revenue = RevenueTracker.get_revenue_summary(db, days=7)
        week_expenses = ExpenseTracker.get_expense_summary(db, days=7)
        
        # Month
        month_revenue = RevenueTracker.get_revenue_summary(db, days=30)
        month_expenses = ExpenseTracker.get_expense_summary(db, days=30)
        
        return {
            "today": {
                "revenue": today_revenue['total'],
                "expenses": today_expenses['total'],
                "profit": ProfitCalculator.calculate_profit(today_revenue['total'], today_expenses['total']),
                "roi": ProfitCalculator.calculate_roi(today_revenue['total'], today_expenses['total'])
            },
            "week": {
                "revenue": week_revenue['total'],
                "expenses": week_expenses['total'],
                "profit": ProfitCalculator.calculate_profit(week_revenue['total'], week_expenses['total']),
                "roi": ProfitCalculator.calculate_roi(week_revenue['total'], week_expenses['total'])
            },
            "month": {
                "revenue": month_revenue['total'],
                "expenses": month_expenses['total'],
                "profit": ProfitCalculator.calculate_profit(month_revenue['total'], month_expenses['total']),
                "roi": ProfitCalculator.calculate_roi(month_revenue['total'], month_expenses['total'])
            }
        }
