from app.databases.sql import Base
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import datetime
from pydantic import Field
from bson import ObjectId
from app.databases.mongo import PyObjectId
import typing as t

from app.models.book.book import Book

class CommentDB(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(10000), nullable=True)
    # timestamp_created = Column(DateTime)
    # timestampe_updated = Column(DateTime)

    book_id = Column(Integer, ForeignKey("books.id"), autoincrement=True)
    book = relationship("app.models.book.book.BookDB", back_populates="comments")


class CommentMongo(BaseModel):
    mongo_id: ObjectId = Field(default_factory=PyObjectId, alias="_id")

    content: t.Optional[str]
    # timestamp_created: datetime
    # timestampe_updated: datetime

    book_id: t.Optional[ObjectId]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: int}



class CommentBase(BaseModel):
    content: t.Optional[str]
    # timestamp_created: datetime
    # timestampe_updated: datetime
    id: t.Optional[int]
    book_id: t.Optional[int]
    # book: Book

    # id: t.Optional[str]

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):

    class Config:
        orm_mode = True