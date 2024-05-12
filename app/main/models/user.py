from app.database.base import Base
from sqlalchemy import Column, String, Integer, DateTime, Text, Identity
from datetime import datetime


class User(Base):
    __tablename__="users"
    __table_args__ = {'extend_existing': True}
    id_identity = Identity(start=1, increment=1)
    id = Column(Integer,id_identity, primary_key=True)
    full_name = Column(String(250), nullable=False)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(Text(), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())
    
    def __repr__(self) -> str:
        return f"<<User id: {self.id}, name:{self.full_name}, created_at: {self.created_at}, updated_at: {self.updated_at} >>"