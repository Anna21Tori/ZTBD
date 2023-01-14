from app.databases.sql import Base
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import datetime
from pydantic import Field
from bson import ObjectId
from app.databases.mongo import PyObjectId

from app.models.book.book import Book

class QuoteDB(Base):
    __tablename__ = "quotes"
    id = Column(String(25), primary_key=True, index=True)
    content = Column(String(10000))
    timestamp_created = Column(DateTime)
    timestampe_updated = Column(DateTime)

    book_id = Column(String(25), ForeignKey("books.id"))
    # book = relationship("app.models.book.book.BookDB", back_populates="reviews")


class QuoteMongo(BaseModel):
    mongo_id: ObjectId = Field(default_factory=PyObjectId, alias="_id")
    id: str
    content: str
    timestamp_created: datetime
    timestampe_updated: datetime

    book_id: ObjectId

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}



class QuoteBase(BaseModel):
    content: str
    timestamp_created: datetime
    timestampe_updated: datetime

    book_id: str
    # book: Book

    id: str

class QuoteCreate(QuoteBase):
    pass

class Quote(QuoteBase):

    class Config:
        orm_mode = True