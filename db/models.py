from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    DateTime,
    Boolean,
)
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Infraction(Base):
    __tablename__ = "infractions"

    id = Column(String, primary_key=True)
    guild_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    moderator_id = Column(BigInteger, nullable=False)
    reason = Column(String, nullable=False)