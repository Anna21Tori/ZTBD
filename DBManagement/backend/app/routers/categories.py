from fastapi import APIRouter, HTTPException
from fastapi import status
from app.models.category.category import Category, CategoryCreate
from app.daos.category.category import CategoryDAO, get_dao

from fastapi import Depends

from app.core.utils import raise_409

router = APIRouter(prefix="/categories")

@router.post("/", response_model=Category)
def create_category(category: CategoryCreate, dao: CategoryDAO = Depends(get_dao)):
    created_category = raise_409(dao.save)(category)
    if not created_category:
        raise HTTPException(status_code=400, detail="already registered")
    return created_category

@router.get("/{id}", response_model=Category)
def get_category_by_id(id: str, dao: CategoryDAO = Depends(get_dao)):
    category = dao.get_by_id(id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return category

def get_categories():
    pass