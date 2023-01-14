from fastapi import APIRouter, HTTPException
from app.models.book.book import Book, BookCreate, BookDB
from app.models.comment.comment import CommentDB
from app.models.quote.quote import QuoteDB
from app.models.catalog.catalog import CatalogCreate
from app.daos.catalog.catalog import CatalogDAO, get_dao

from fastapi import Depends

from app.core.utils import raise_409

router = APIRouter(prefix="/catalog")


@router.post("/", response_model=Book)
def create_catalog(catalog: CatalogCreate, db: str, dao: CatalogDAO = Depends(get_dao)):
    created_book = raise_409(dao.save)(catalog)
    if not created_book:
        raise HTTPException(status_code=400, detail="already registered")
    return created_book
