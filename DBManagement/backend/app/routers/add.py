from fastapi import APIRouter, HTTPException
from app.models.test.test import ResultTest, ResultFiltersTest
from app.repository_test import RepositoryAddTest, RepositoryDelTest, RepositoryFiltersTest
from fastapi import Depends

router = APIRouter(prefix="/test")

@router.get("/insert", response_model=ResultTest)
def get_insert_test(dao: RepositoryAddTest = Depends(RepositoryAddTest)):
    return dao.get()

@router.get("/delete", response_model=ResultTest)
def get_delete_test(dao: RepositoryDelTest = Depends(RepositoryDelTest)):
    return dao.get()

@router.get("/filters", response_model=ResultFiltersTest)
def get_delete_test(dao: RepositoryFiltersTest = Depends(RepositoryFiltersTest)):
    return dao.get()