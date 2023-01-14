from app.databases.sql import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from app.databases.mongo import PyObjectId
from bson import ObjectId
from datetime import datetime
 
class BookDB(Base):
    __tablename__ = "books"
    id = Column(String(25), primary_key=True, index=True)
    title = Column(str)
    isbn = Column(str)
    description = Column(str)
    orginal_name = Column(str)
    pages = Column(Integer)
    lang = Column(str)
    date = Column(DateTime)
    pol_date = Column(DateTime)
    author = Column(str)
    publishing = Column(str)
    translator = Column(str)

    comments = relationship("app.models.comment.comment.CommentDB", back_populates="book", lazy="dynamic")
    quotes = relationship("app.models.quote.quote.QuoteDB", back_populates="book", lazy="dynamic")
    categories = relationship("app.models.category.category.CategoryDB", back_populates="book", lazy="dynamic")

class BookMongo(BaseModel):
    mongo_id: ObjectId = Field(default_factory=PyObjectId, alias="_id")
    id: str
    title: str
    isbn: str
    description: str
    orginal_name: str
    pages: int
    lang: str
    date: DateTime
    pol_date: DateTime
    author_id: str
    publishing_id: str
    translator_id: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class BookBase(BaseModel):
    title: str
    isbn: str
    description: str
    orginal_name: str
    pages: int
    lang: str
    date: datetime
    pol_date: datetime
    author: str
    publishing: str
    translator: str
    
    id: str

class BookCreate(BookBase):
    pass

class Book(BookBase):

    class Config:
        orm_mode = True
