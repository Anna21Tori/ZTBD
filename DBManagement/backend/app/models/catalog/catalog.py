from app.models.book.book import BookCreate
from app.models.comment.comment import CommentCreate
from app.models.quote.quote import QuoteCreate
from app.models.category.category import CategoryCreate
import typing as t
from pydantic import BaseModel

class CatalogBase(BaseModel):
    book: BookCreate
    comments: t.List[CommentCreate]
    quotes: t.List[QuoteCreate]
    categories: t.List[CategoryCreate]

class CatalogCreate(CatalogBase):
    pass