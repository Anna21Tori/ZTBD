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

class CategoryDB(Base):
    __tablename__ = "categotries"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(10000), nullable=True)

    book_id = Column(Integer, ForeignKey("books.id"))
    book = relationship("app.models.book.book.BookDB", back_populates="categories")


class CategoryMongo(BaseModel):
    mongo_id: ObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: t.Optional[str]

    book_id: t.Optional[ObjectId]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: int}



class CategoryBase(BaseModel):
    name: t.Optional[str]
    id: t.Optional[int]
    book_id: t.Optional[int]
    # book: Book

    # id: t.Optional[str]

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):

    class Config:
        orm_mode = True