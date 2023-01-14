from fastapi import APIRouter, HTTPException
from app.models.book.book import Book, BookCreate, BookDB
from app.models.comment.comment import CommentDB
from app.models.quote.quote import QuoteDB
from app.models.category.category import CategoryDB
from app.daos.book.book import BookDAO, get_dao

from fastapi import Depends

from app.core.utils import raise_409

router = APIRouter(prefix="/books")


@router.post("/", response_model=Book)
def create_book(book: BookCreate, db: str, dao: BookDAO = Depends(get_dao)):
    created_book = raise_409(dao.save)(book)
    if not created_book:
        raise HTTPException(status_code=400, detail="already registered")
    return created_book

@router.get("/{id}", response_model=Book)
def get_book_by_id(id: str, db: str, dao: BookDAO = Depends(get_dao)):
    book = dao.get_by_id(id)
    return book

def get_books():
    pass