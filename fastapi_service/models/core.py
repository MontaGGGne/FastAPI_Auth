from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    s3_folder_id = Column(UUID, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    
    items = relationship("Item", back_populates="owner", passive_deletes=True)
    tokens = relationship("Token", back_populates="user", passive_deletes=True)


class Token(Base):
    __tablename__ = "tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))

    user = relationship("User", back_populates="tokens")


class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    s3_path = Column(String, unique=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    
    owner = relationship("User", back_populates="items")