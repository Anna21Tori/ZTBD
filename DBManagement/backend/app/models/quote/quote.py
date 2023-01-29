from app.databases.sql import Base
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import datetime
from pydantic import Field
from bson import ObjectId
from app.databases.mongo import PyObjectId
import typing as t


class QuoteDB(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content = Column(String(10000), nullable=True)
    # timestamp_created = Column(DateTime)
    # timestampe_updated = Column(DateTime)

    book_id = Column(Integer, ForeignKey("books.id"))
    book = relationship("app.models.book.book.BookDB", back_populates="quotes")


class QuoteMongo(BaseModel):
    mongo_id: ObjectId = Field(default_factory=PyObjectId, alias="_id")
    content: t.Optional[str]
    # timestamp_created: datetime
    # timestampe_updated: datetime

    # book_id: t.Optional[ObjectId]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: int}



class QuoteBase(BaseModel):
    content: t.Optional[str]
    id: t.Optional[int]
    # timestamp_created: datetime
    # timestampe_updated: datetime

    book_id: t.Optional[int]
    # book: Book

    # id: t.Optional[str]

class QuoteCreate(QuoteBase):
    pass

class QuoteRedis(QuoteBase):
    pass

class Quote(QuoteBase):

    class Config:
        orm_mode = True