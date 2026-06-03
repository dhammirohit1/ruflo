from sqlalchemy import Column, String, Float, DateTime, Boolean, Integer, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    role = Column(String(100), nullable=False)
    level = Column(Integer, nullable=False)
    status = Column(String(20), default="idle")  # idle, active, learning, error
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    performance_score = Column(Float, default=0.0)
    tasks_completed = Column(Integer, default=0)

class Business(Base):
    __tablename__ = "businesses"
    
    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    business_type = Column(String(100), nullable=False)  # saas, affiliate, ecommerce, etc
    status = Column(String(20), default="pending")  # pending, launching, active, scaling, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    launched_at = Column(DateTime)
    revenue = Column(Float, default=0.0)
    expenses = Column(Float, default=0.0)
    profit = Column(Float, default=0.0)
    roi = Column(Float, default=0.0)
    agent_id = Column(String(36))

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(String(36), primary_key=True)
    type = Column(String(50), nullable=False)  # bank_transfer, crypto_transfer, paypal_transfer, income
    status = Column(String(20), default="pending")  # pending, completed, failed
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")
    source = Column(String(100))
    destination = Column(String(100))
    transaction_ref = Column(String(255))  # External API reference
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    error_message = Column(Text)
    metadata = Column(Text)  # JSON metadata

class Revenue(Base):
    __tablename__ = "revenue"
    
    id = Column(String(36), primary_key=True)
    business_id = Column(String(36))
    amount = Column(Float, nullable=False)
    source = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    date = Column(DateTime, nullable=False)

class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(String(36), primary_key=True)
    business_id = Column(String(36))
    agent_id = Column(String(36))
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    date = Column(DateTime, nullable=False)

class Opportunity(Base):
    __tablename__ = "opportunities"
    
    id = Column(String(36), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    opportunity_type = Column(String(100), nullable=False)  # affiliate, saas, lead_gen, etc
    market_score = Column(Float, default=0.0)  # 0-100
    revenue_score = Column(Float, default=0.0)  # 0-100
    risk_score = Column(Float, default=0.0)  # 0-100
    competition_score = Column(Float, default=0.0)  # 0-100
    time_to_profit_score = Column(Float, default=0.0)  # 0-100
    status = Column(String(20), default="discovered")  # discovered, evaluated, approved, launched, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    evaluated_at = Column(DateTime)
    launcher_agent_id = Column(String(36))

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String(36), primary_key=True)
    action = Column(String(100), nullable=False)
    actor = Column(String(100), nullable=False)  # agent_id or owner
    resource_type = Column(String(50))
    resource_id = Column(String(36))
    details = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
