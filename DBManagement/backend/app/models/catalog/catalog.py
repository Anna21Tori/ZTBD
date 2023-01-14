from app.models.book.book import BookCreate
from app.models.comment.comment import CommentCreate
from app.models.quote.quote import QuoteCreate
from app.models.category.category import CategoryCreate
import typing as t

class CatalogCreate:
    book: BookCreate
    comments: t.List[CommentCreate]
    quotes: t.List[QuoteCreate]
    categories: t.List[CategoryCreate]