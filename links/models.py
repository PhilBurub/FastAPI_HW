from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

class Credentials(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, index=True, nullable=False)
    token = Column(String, nullable=False)

class Links(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, index=True, nullable=False)
    alias = Column(String, unique=True, index=True, nullable=False)
    created = Column(DateTime, nullable=False)
    last_accessed = Column(DateTime)
    times_accessed = Column(Integer, default=0, nullable=False)
    expires_at = Column(DateTime)
