import argparse
import requests
from dataclasses import dataclass
import csv
import logging 
import aiohttp
import asyncio
import os
import typing as t
import json

# BATCH_SIZE = 5000
# ALL_RECORDS_COUNT = 48296895 / BATCH_SIZE

@dataclass
class Book:
    title: str
    description: str
    isbn: str
    publishing: str
    author: str
    orginal_name: str
    date: str
    pol_date: str
    pages: str
    lang: str
    translator: str
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


@dataclass
class Comment:
    content: str
    book_id: t.Optional[int] = None
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

@dataclass
class Quote:
    content: str
    book_id: t.Optional[int] = None
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

@dataclass
class Category:
    name: str
    book_id: t.Optional[int] = None
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
@dataclass
class Catalog:
    book: Book
    comments: t.List[Comment]
    quotes: t.List[Quote]
    categories: t.List[Category]

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


# session = requests.session()
async def add_book(session: aiohttp.ClientSession, book: Book, url: str, db: str):
    async with session.post(f"{url}/books/", params={"db": db}, json={
        "title": book.title,
        "isbn": book.isbn,
        "description": book.description,
        "orginal_name": book.orginal_name,
        "pages": book.pages,
        "lang": book.lang,
        "date": book.date,
        "pol_date": book.pol_date,
        "author": book.author,
        "publishing": book.publishing,
        "translator": book.translator
    }) as resp:
        if resp.status == 200:
            logging.info(f"added {book.title} {resp}") 
        elif resp.status == 409:
            logging.debug(f"already exists {book.title}")

async def add_comment_async(session: aiohttp.ClientSession, comment: Comment, url: str, db: str):
    async with session.post(f"{url}/comments/", params={"db": db}, json={
        "content": comment.content,
        "book_id": comment.book_id

    }) as resp:
        if resp.status == 200:
            logging.info(f"added comment") 
        elif resp.status == 409:
            logging.debug(f"already exists comment")
        else:
            raise Exception(f"status code: {resp.status}")

async def add_quote_async(session: aiohttp.ClientSession, quote: Quote, url: str, db: str):
    async with session.post(f"{url}/quotes/", params={"db": db}, json={
        "content": quote.content,
        "book_id": quote.book_id

    }) as resp:
        if resp.status == 200:
            logging.info(f"added quote") 
        elif resp.status == 409:
            logging.debug(f"already exists quote")
        else:
            raise Exception(f"status code: {resp.status}")

async def add_category_async(session: aiohttp.ClientSession, category: Category, url: str, db: str):
    async with session.post(f"{url}/categories/", params={"db": db}, json={
        "name": category.name,
        "book_id": category.book_id

    }) as resp:
        if resp.status == 200:
            logging.info(f"added {category.name}") 
        elif resp.status == 409:
            logging.debug(f"already exists {category.name}")
        else:
            raise Exception(f"status code: {resp.status}")
        
async def add_catalog_async(session: aiohttp.ClientSession, catalog: str, url: str, db: str):
    async with session.post(f"{url}/catalog/", params={"db": db}, json=catalog)as resp:
        if resp.status == 200:
            logging.info(f"added catalog {resp}") 
        elif resp.status == 409:
            logging.debug(f"already exists catalog")
        else:
            raise Exception(f"status code: {resp}")

async def batch_process(records: t.List[Catalog], url: str, db: str):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for record in records:
            tasks.append(asyncio.ensure_future(add_book(session, record.book, url, db)))
        
        results = await asyncio.gather(*tasks)
        #print(results[0])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file")
    parser.add_argument("--url")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    for db in ["mongodb", "postgresql"]:
        for file in os.listdir("./storage"):
            with open(f"./storage/{file}", encoding="utf8") as file_obj:
                # Skips the heading
                    # Using next() method
                    heading = next(file_obj)

                    # Create reader object by passing the file
                    # object to reader method
                    reader_obj = csv.reader(file_obj)

                    # Iterate over each row in the csv file
                    # using reader object
                    for row in reader_obj:
                        title = row[0].strip()
                        author = row[1].strip()
                        categories = []
                        if row[2] != '':
                            categories = row[2].strip().split(sep=',')
                        publishing = row[3].strip()
                        isbn = row[4].strip()
                        description = row[5].strip()
                        originalTitle = row[6].strip()
                        date = None
                        if row[7] != '':
                            date = row[7].strip()
                        datePol = None
                        if row[8] != '':
                            datePol = row[8].strip()
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
                            
                    _book: Book = Book(title=title, 
                                        description=description, 
                                        isbn=isbn, 
                                        publishing=publishing, 
                                        author=author, 
                                        orginal_name=originalTitle, 
                                        date=date, 
                                        pol_date=datePol, 
                                        pages=pages, 
                                        lang=lang, 
                                        translator=translator)
                    
                    _comments: t.List[Comment] = []
                    for comment in comments:
                        _comments.append(Comment(content=comment))
                        
                    _quotes: t.List[Quote] = []
                    for quote in quotes:
                        _quotes.append(Comment(content=quote))
                        
                    _categories: t.List[Category] = []
                    for category in categories:
                        _categories.append(Comment(content=category))
                        
                    catalog: Catalog = Catalog(book=_book, comments=_comments, quotes=_quotes, categories=_categories)
                    asyncio.run(batch_process([catalog], args.url, db))

                


                


if __name__ == "__main__":
    main()
