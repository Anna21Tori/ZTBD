from app.models.book.book import BookCreate
from app.models.comment.comment import CommentCreate
from app.models.quote.quote import QuoteCreate
from app.models.category.category import CategoryCreate
from app.repository import Book
import os
import csv
import datetime
import typing as t

def load_all_records():
    
    book_id = 1
    comment_id = 1
    quote_id = 1
    category_id = 1

    repo: t.List[Book] = []


    files = ["books_50.csv", "books_100.csv", "books_150.csv", "books_200.csv", "books_250.csv", "books_300.csv", "books_350.csv", "books_400.csv", "books_450.csv", "books_550.csv", "books_500.csv", "books_600.csv"]

    for file in os.listdir("./storage"):
        with open(f"./storage/{file}", encoding="utf8") as file_obj:
            
            heading = next(file_obj)
            reader_obj = csv.reader(file_obj)

            for row in reader_obj:
                item: Book = Book(book=None, quotes=[], categories=[], comments=[])

                title = row[0].strip()
                author = row[1].strip()
                categories = []
                if row[2] != '':
                    categories = row[2].strip().split(sep=',')
                publishing = row[3].strip()
                isbn = row[4].strip()
                description = row[5].strip()
                originalTitle = row[6].strip()
                _date = None
                if row[7] != '':
                    data = row[7].strip().split(sep="-")
                    _date = datetime.datetime(year=int(data[0]), month=int(data[1]), day=int(data[2]))
                datePol = None
                if row[8] != '':
                    data = row[8].strip().split(sep="-")
                    datePol = datetime.datetime(year=int(data[0]), month=int(data[1]), day=int(data[2]))
                pages = 0
                if row[9] != '':
                    pages = int(row[9].strip())
                lang = row[10].strip()
                translator = row[11].strip()
                comments = []
                if row[12] != '':
                    comments = row[12].strip().split(sep=',')
                quotes = []
                if row[13] != '':
                    quotes = row[13].strip().split(sep=',')
                            
                _book: BookCreate = BookCreate(
                    id= book_id,
                    title=title, 
                    description=description, 
                    isbn=isbn, 
                    publishing=publishing, 
                    author=author, 
                    orginal_name=originalTitle, 
                    date=_date, 
                    pol_date=datePol, 
                    pages=pages, 
                    lang=lang, 
                    translator=translator)
                
                for comment in comments:
                    if comment != "":
                        _comment: CommentCreate = CommentCreate(content=comment, id=comment_id, book_id=book_id)
                        item.comments.append(_comment)
                        comment_id +=1
                                
                for quote in quotes:
                    if quote != "":
                        _quote: CommentCreate = CommentCreate(content=quote, id=quote_id, book_id=book_id)
                        item.quotes.append(_quote)
                        quote_id += 1
                                
                for category in categories:
                    if category != '':
                            _category: CategoryCreate = CategoryCreate(name=category, id=category_id, book_id=book_id)
                            item.categories.append(_category)
                            category_id += 1

                book_id += 1
                item.book = _book
                repo.append(item)
                
            print(f"Records from file '{file}' were loaded")

    return repo
