import redis
from app.core.config import settings
from enum import Enum

from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query
from redis import exceptions

class RedisDbs(Enum):
    BOOKS = 0
    CATEGORIES = 0
    COMMENTS = 0
    QUOTES = 0

redisInstanceBooks = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, db=RedisDbs.BOOKS.value)
redisInstanceCategories = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, db=RedisDbs.CATEGORIES.value)
redisInstanceComments = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, db=RedisDbs.COMMENTS.value)
redisInstanceQuotes = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, db=RedisDbs.QUOTES.value)
schema = (TextField("$.comment_id", as_name="comment_id"),TextField("$.category_id", as_name="category_id"),TextField("$.quote_id", as_name="quote_id"))
try:
    info = redisInstanceBooks.ft('books_idx').info()
except exceptions.ResponseError as e:
    print("adding index")
    redisInstanceBooks.ft('books_idx').create_index(schema, definition=IndexDefinition(prefix=["book:"], index_type=IndexType.JSON))


def get_redis(db: RedisDbs) -> redis.Redis:
    if db == RedisDbs.BOOKS:
        return redisInstanceBooks
    elif db == RedisDbs.CATEGORIES:
        return redisInstanceCategories
    elif db == RedisDbs.COMMENTS:
        return redisInstanceComments
    elif db == RedisDbs.QUOTES:
        return redisInstanceQuotes
    else:
        raise ValueError("no such db in redis")