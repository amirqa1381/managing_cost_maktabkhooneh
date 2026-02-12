from database_test import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime, Table,UniqueConstraint, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30), nullable=False, unique=True)
    email = Column(String(), nullable=False, unique=True)
    password = Column(String(), nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    
    costs = relationship("Costs", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"(id={self.id} , username={self.username}, email={self.email})"
    
    


class Costs(Base):
    __tablename__ = "costs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id"), nullable=False, index=True)
    description = Column(String(255), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("Users", back_populates="costs")
    