from fastapi import APIRouter, HTTPException
from fastapi import status
from app.models.comment.comment import Comment, CommentCreate
from app.daos.comment.comment import CommentDAO, get_dao

from fastapi import Depends

from app.core.utils import raise_409

router = APIRouter(prefix="/comments")

@router.post("/", response_model=Comment)
def create_comment(comment: CommentCreate, dao: CommentDAO = Depends(get_dao)):
    created_comment = raise_409(dao.save)(comment)
    if not created_comment:
        raise HTTPException(status_code=400, detail="already registered")
    return created_comment

@router.get("/{id}", response_model=Comment)
def get_comment_by_id(id: str, dao: CommentDAO = Depends(get_dao)):
    comment = dao.get_by_id(id)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return comment

def get_comments():
    pass