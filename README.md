# ZTBD - DB Performance Tester

## Setup
  - cd .\DBManagement
  - docker compose-up
  
## Run tests
  - cd .\DBManagement\backend
  - python -m venv .venv
  - .\.venv\Scripts\activate
  - pip install -r .\requirements.txt
  - python main.py --test add_books_mongo
  - python main.py --test add_books_redis
  - python main.py --test add_books_postgresql
  - python main.py --test del_books_mongo
  - python main.py --test del_books_postgresql
  - python main.py --test filter_books_mongo
  - python main.py --test filter_books_postgresql
  
 ## View DB performance results
 
  ### Run API
    - cd .\DBManagement\backend
    - .\.venv\Scripts\activate
    - python -m uvicorn app.main:app --reload
  
  ### Run front
    - before run install nodejs
    - cd .\DBManagement\front
    - npm i
    - npm run start
  
