from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from database.db import Base
from datetime import datetime


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    email = Column(String, unique=True)

    password = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Income(Base):

    __tablename__ = "income"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    amount = Column(Float)

    date = Column(
        DateTime,
        default=datetime.utcnow
    )



class Expense(Base):

    __tablename__ = "expenses"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    amount = Column(Float)

    category = Column(String)

    description = Column(String)

    date = Column(DateTime)
    
class Goal(Base):

    __tablename__ = "goals"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    goal_name = Column(String)

    target_amount = Column(Float)

    saved_amount = Column(
        Float,
        default=0
    )

    deadline = Column(DateTime)