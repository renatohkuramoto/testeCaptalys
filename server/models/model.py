from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.types import PickleType
from sqlalchemy.orm import relationship
from server.database import Base


class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)
    username = Column(String(255), index=True)
    repositories = Column(PickleType)
    
    repo = relationship("Repositories")
    

class Repositories(Base):
    __tablename__ = "repositories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    repo_id = Column(Integer, unique=True, index=True)
    url = Column(String(255))
    name = Column(String(255))
    access_type = Column(String(50))
    created_at = Column(String(50))
    updated_at = Column(String(50))
    size = Column(Integer)
    stargazers_count = Column(Integer)
    watchers_count = Column(Integer)
