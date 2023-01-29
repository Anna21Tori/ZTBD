# ZTBD - DB Performance Tester

## Setup
  - Make file .\DBManagement\backend.env which consists of following config
  ```
    PROJECT_NAME=DBManagement
    BACKEND_CORS_ORIGINS=["http://localhost:8000", "https://localhost:8000", "http://localhost", "https://localhost", "http://localhost:3000",         "https://localhost:3000", "*"]
    DATABASE_URI="sqlite:///./sql_app.db"

    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_SERVER=database
    POSTGRES_DB=app
    REDIS_HOST=localhost
    REDIS_PORT=6379
    REDIS_URI="redis://localhost:password@localhost:6379"
    MONGODB_URI="mongodb://root:example@localhost:27017"
  ```
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
  
