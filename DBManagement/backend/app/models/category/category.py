from app.databases.sql import Base
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import datetime
from pydantic import Field
from bson import ObjectId
from app.databases.mongo import PyObjectId

from app.models.book.book import Book

class CategoryDB(Base):
    __tablename__ = "categotries"
    id = Column(String(25), primary_key=True, index=True)
    name = Column(String(10000))

    book_id = Column(String(25), ForeignKey("books.id"))
    # book = relationship("app.models.book.book.BookDB", back_populates="reviews")


class CategoryMongo(BaseModel):
    mongo_id: ObjectId = Field(default_factory=PyObjectId, alias="_id")
    id: str
    name: str

    book_id: ObjectId

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}



class CategoryBase(BaseModel):
    name: str

    book_id: str
    # book: Book

    id: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):

    class Config:
        orm_mode = True