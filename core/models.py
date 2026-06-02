from datetime import datetime, timezone
from core.database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Text,
    DateTime,
    Table,
    UniqueConstraint,
    Numeric,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2"],
    default="argon2",
    deprecated="auto",
    argon2__memory_cost=65536,  # 64 MB
    argon2__time_cost=3,
    argon2__parallelism=4,
)


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(String, default=datetime.now(timezone.utc))
    revoked = Column(Boolean, default=False)

    user = relationship("Users", back_populates="refresh_tokens")


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

    refresh_tokens = relationship("RefreshToken", back_populates="user")
    costs = relationship("Costs", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"(id={self.id} , username={self.username}, email={self.email})"

    def hash_password(self, plain_password: str):
        """
        this method is for hashing the password of the user

        Args:
            plain_password (str): password that we pass for hashing
        """

        hashed_password = pwd_context.hash(plain_password)
        return hashed_password

    def verify_password(self, plain_password: str):
        """
        this method is for verifying the passwords

        Args:
            plain_password (str): this is the password that we get for checking
        """
        return pwd_context.verify(plain_password, str(self.password))

    def set_password(self, plain_password: str):
        """
        Method for setting the hash password for user

        Args:
            plain_password (str): password that user insert
        """
        self.password = self.hash_password(plain_password)


class Costs(Base):
    __tablename__ = "costs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id"), nullable=False, index=True)
    description = Column(String(255), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("Users", back_populates="costs")
