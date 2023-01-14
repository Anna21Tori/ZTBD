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
    ISBN: str
    publishing: str
    author: str
    orginalTitle: str
    date: str
    datePol: str
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
    comments: t.List[str]
    quotes: t.List[str]
    categories: t.List[str]

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

# session = requests.session()
def add_book(book: Book, url: str, db: str):
    resp = requests.post(f"{url}/books/", params={"db": db}, json={
        "title": book.title,
        "isbn": book.ISBN,
        "description": book.description,
        "orginal_name": book.orginalTitle,
        "pages": book.pages,
        "lang": book.lang,
        "date": book.date,
        "pol_date": book.datePol,
        "author": book.author,
        "publishing": book.publishing,
        "translator": book.translator
    })
    if resp.status_code == 200:
        logging.info(f"added {book.title}") 
    elif resp.status_code == 409:
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
    async with session.post(f"{url}/categoriess/", params={"db": db}, json={
        "name": category.name,
        "book_id": category.book_id

    }) as resp:
        if resp.status == 200:
            logging.info(f"added {category.name}") 
        elif resp.status == 409:
            logging.debug(f"already exists {category.name}")
        else:
            raise Exception(f"status code: {resp.status}")
        
async def add_catalog_async(session: aiohttp.ClientSession, catalog: Catalog, url: str, db: str):
    async with session.post(f"{url}/catalog/", params={"db": db}, json={
        "book": catalog.book,
        "comments": catalog.comments,
        "quotes": catalog.quotes,
        "categories": catalog.categories

    }) as resp:
        if resp.status == 200:
            logging.info(f"added catalog") 
        elif resp.status == 409:
            logging.debug(f"already exists catalog")
        else:
            raise Exception(f"status code: catalog")

async def batch_process(records, url: str, db: str):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for record in records:
            tasks.append(asyncio.ensure_future(add_catalog_async(session, record, url, db)))
        
        results = await asyncio.gather(*tasks)
        # print(results[0])

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
                                        ISBN=isbn, 
                                        publishing=publishing, 
                                        author=author, 
                                        orginalTitle=originalTitle, 
                                        date=date, 
                                        datePol=datePol, 
                                        pages=pages, 
                                        lang=lang, 
                                        transator=translator)
                    
                    _comments: t.List[str] = []
                    for comment in comments:
                        _comments.append(Comment(content=comment).to_json())
                        
                    _quotes: t.List[str] = []
                    for quote in quotes:
                        _quotes.append(Comment(content=quote))
                        
                    _categories: t.List[str] = []
                    for category in categories:
                        _categories.append(Comment(content=category).to_json())
                        
                    catalog: Catalog = Catalog(book=_book.to_json(), comments=_comments, quotes=_quotes, categories=_categories)
                    asyncio.run(batch_process([catalog], args.url, db))
                
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--file")
    # parser.add_argument("--url")
    # args = parser.parse_args()

    # logging.basicConfig(level=logging.INFO)

    # records_batch = []
    # with open(args.file) as rfile:
    #     reader = csv.DictReader(rfile)
    #     with Bar('Processing', max=ALL_RECORDS_COUNT, suffix = '%(percent).1f%% - %(eta_td)s ') as bar:
    #         for db in ["mongodb", "postgresql"]:
    #             for i, row in enumerate(reader):
    #                 logging.debug(f"processing - {db} - {i}")
    #                 row.pop('')
    #                 row = {k.replace(".", "_"):v for k,v in row.items()}

    #                 record = Record(**row)
    #                 records_batch.append(record)
                    
    #                 if len(records_batch)%BATCH_SIZE == 0:
    #                     logging.info(f"processing batch - {i}")
    #                     asyncio.run(batch_process(records_batch, args.url, db))
    #                     records_batch = []
    #                     bar.next()


                


if __name__ == "__main__":
    main()
