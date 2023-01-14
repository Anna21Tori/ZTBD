from fastapi import APIRouter, HTTPException
from fastapi import status
from app.models.quote.quote import Quote, QuoteCreate
from app.daos.quote.quote import QuoteDAO, get_dao

from fastapi import Depends

from app.core.utils import raise_409

router = APIRouter(prefix="/quotes")

@router.post("/", response_model=Quote)
def create_quote(quote: QuoteCreate, dao: QuoteDAO = Depends(get_dao)):
    created_quote = raise_409(dao.save)(quote)
    if not created_quote:
        raise HTTPException(status_code=400, detail="already registered")
    return created_quote

@router.get("/{id}", response_model=Quote)
def get_quote_by_id(id: str, dao: QuoteDAO = Depends(get_dao)):
    quote = dao.get_by_id(id)
    if quote is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return quote

def get_quotes():
    pass