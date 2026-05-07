from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import ForeignKey, String, Integer, Column, DateTime, func
from sqlalchemy import Uuid
import uuid
from datetime import datetime
from typing import Optional, List


class User(SQLModel, table=True):
    __tablename__ = "User"
    user_id:uuid.UUID = Field(sa_column=Column(Uuid, nullable=False, primary_key=True, default=uuid.uuid4))
    username:str
    password:str
    email:str
    urls:List["UrlMapper"]= Relationship(back_populates="user")
    created_at:datetime=Field(sa_column=Column(DateTime, default=func.now()))
    updated_at:datetime=Field(sa_column=Column(DateTime, default=func.now()))


class UrlMapper(SQLModel, table=True):
    __tablename__ = "URLMapper"
    url_id:uuid.UUID = Field(sa_column=Column(Uuid, nullable=False, primary_key=True, default=uuid.uuid4))
    user_id: Optional[uuid.UUID] = Field(sa_column=Column(Uuid, ForeignKey("User.user_id"), nullable=True), default=None)
    user: Optional["User"] = Relationship(back_populates="urls")
    title:str = Field(default="My link")
    url:str
    shortened_url:str
    num_visits:int = Field(default=0)
    created_at:datetime=Field(sa_column=Column(DateTime, default=func.now()))
    updated_at:datetime=Field(sa_column=Column(DateTime, default=func.now()))