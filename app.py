import requests
import typing as t
import re
import csv
from bs4 import BeautifulSoup
from models import BookModel
header = ['title', 'author', 'categories', 'publishing', "isbn", 'description', "orginalTitle", "date", "datePol", "pages", "lang", "translator", "comments", "quotes"]

api = "https://lubimyczytac.pl"
def getPagination():

    URL = f"{api}/katalog"
    main = requests.get(URL)
    soup = BeautifulSoup(main.content, "html.parser")
    pagination = int(soup.find(class_="paginationList__info").find("span").get_text().replace(" ", ""))
    return pagination

current = 5850
offset = 50

pagination = current#getPagination()
counter = 0
with open(f'books_{current}.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for i in range(current - offset, pagination):
        url = f"{api}/katalog?page={i}"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser", from_encoding="utf-8")

        books = soup.select(".authorAllBooks__single")
        for book in books:
            model: BookModel = BookModel(id=counter, title="", categories="", content="", ISBN="", publishing="", author="", date="", datePol="", pages="", lang="", transator="", comments="", quotes="", orginalTitle="")
            counter+=1
            titleTag = book.find(class_="authorAllBooks__singleTextTitle")
            model.title = titleTag.get_text()

            href = titleTag["href"]
            urlBook = f"{api}{href}"
            bookPage = requests.get(urlBook)
            bookSoup = BeautifulSoup(bookPage.content, "html.parser", from_encoding="utf-8")

            authorTag = bookSoup.find(class_="author")
            if authorTag != None:
                if authorTag.find("a") != None:
                    model.author = authorTag.find("a").get_text()

            publishingTag = bookSoup.find(class_="book__txt")
            if publishingTag != None and publishingTag.find("a") != None:
                model.publishing = publishingTag.find("a").get_text()
            
            categoriesTag = bookSoup.find(class_="book__category")
            if categoriesTag != None:
                model.categories = categoriesTag.get_text()

            isbnTag = bookSoup.find("dt", text = re.compile('ISBN:'))
            if isbnTag != None:
                model.ISBN = isbnTag.find_next_sibling().get_text()

            contentTag = bookSoup.find(class_="collapse-content")
            if contentTag != None and contentTag.find("p"):
                model.content = contentTag.find("p").get_text()

            orginalTitleTag = bookSoup.find("dt", text = re.compile('Tytuł oryginału:'))
            if orginalTitleTag!= None:
                model.orginalTitle = orginalTitleTag.find_next_sibling().get_text()
            
            dateTag = bookSoup.find("dt", text = re.compile('Data wydania:'))
            if dateTag!= None:
                model.date = dateTag.find_next_sibling().get_text()

            datePolTag = bookSoup.find("dt", text = re.compile('Data 1. wyd. pol.:'))
            if datePolTag!= None:
                model.datePol = datePolTag.find_next_sibling().get_text()
            
            pagesTag = bookSoup.find("dt", text = re.compile('Liczba stron:'))
            if pagesTag!= None:
                model.pages = pagesTag.find_next_sibling().get_text()

            langTag = bookSoup.find("dt", text = re.compile('Język:'))
            if langTag!= None:
                model.lang = langTag.find_next_sibling().get_text()

            transatorTag = bookSoup.find("dt", text = re.compile('Tłumacz:'))
            if transatorTag!= None:
                model.transator = transatorTag.find_next_sibling().get_text()
            
            commentTags = bookSoup.select(".comment-cloud__body")
            comments: str = []
            if commentTags != None:
                for tag in commentTags:
                    comments.append(tag.get_text())
            model.comments = ";".join(comments)

            quoteTags = bookSoup.select(".quote")
            quotes: str = []
            if quoteTags != None:
                for tag in quoteTags:
                    quote = tag.find(class_="js-expanded")
                    if quote != None:
                        quotes.append(quote.get_text())
            model.quotes = ";".join(quotes)

            data = [model.title, model.author, model.categories, model.publishing, model.ISBN, model.content, model.orginalTitle, model.date, model.datePol, model.pages, model.lang, model.transator, model.comments, model.quotes]
            writer.writerow(data)
