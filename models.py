from pydantic import BaseModel

class BookModel(BaseModel):
    id: int
    title: str
    categories: str
    content: str
    ISBN: str
    publishing: str
    author: str
    orginalTitle: str
    date: str
    datePol: str
    pages: str
    lang: str
    transator: str
    comments: str
    quotes: str