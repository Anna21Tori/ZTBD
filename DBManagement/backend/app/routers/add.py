from fastapi import APIRouter, HTTPException
from app.models.test.test import AddTest
from app.repository_test import RepositoryAddTest
from fastapi import Depends

router = APIRouter(prefix="/add_test")

@router.get("/", response_model=AddTest)
def get_authors(dao: RepositoryAddTest = Depends(RepositoryAddTest)):
    return dao.get()