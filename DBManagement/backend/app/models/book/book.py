from app.databases.sql import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from app.databases.mongo import PyObjectId
from bson import ObjectId
from datetime import datetime
import typing as t
from app.models.comment.comment import CommentMongo
from app.models.category.category import CategoryMongo
from app.models.quote.quote import QuoteMongo
import json
class BookDB(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(1000))
    isbn = Column(String(1000))
    description = Column(String(1000))
    orginal_name = Column(String(1000))
    pages = Column(Integer)
    lang = Column(String(1000))
    date = Column(DateTime, unique=False, nullable=True)
    pol_date = Column(DateTime, unique=False, nullable=True)
    author = Column(String(1000))
    publishing = Column(String(1000))
    translator = Column(String(1000))

    
    quotes = relationship("app.models.quote.quote.QuoteDB", back_populates="book")
    comments = relationship("app.models.comment.comment.CommentDB", back_populates="book")
    categories = relationship("app.models.category.category.CategoryDB", back_populates="book")

class BookMongo(BaseModel):
    mongo_id: ObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    isbn: t.Optional[str]
    description: t.Optional[str]
    orginal_name: t.Optional[str]
    pages: t.Optional[int]
    lang: t.Optional[str]
    date: t.Optional[datetime]
    pol_date: t.Optional[datetime]
    author: t.Optional[str]
    publishing: t.Optional[str]
    translator: t.Optional[str]
    comments: t.Optional[t.List[CommentMongo]]
    categories: t.Optional[t.List[CategoryMongo]]
    quotes: t.Optional[t.List[QuoteMongo]]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: int}


class BookBase(BaseModel):
    title: str
    id: t.Optional[int]
    isbn: t.Optional[str]
    description: t.Optional[str]
    orginal_name:t.Optional[str]
    pages: t.Optional[int]
    lang: t.Optional[str]
    date: t.Optional[datetime]
    pol_date: t.Optional[datetime]
    author: t.Optional[str]
    publishing: t.Optional[str]
    translator: t.Optional[str]
    

class BookCreate(BookBase):
    pass

class BookRedis(BookBase):
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class Book(BookBase):
    class Config:
        orm_mode = True
