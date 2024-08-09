from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost/event_sourcing_db"

Base = declarative_base()


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True)  # e.g., "deposit", "withdrawal"
    amount = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    account_id = Column(Integer, index=True)


class Snapshot(Base):
    __tablename__ = "snapshots"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, index=True)
    balance = Column(Float)
    last_event_id = Column(Integer, ForeignKey("events.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


# Setting up the database engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
