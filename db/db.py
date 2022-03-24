from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import DATABASE_URL
Base = declarative_base()

# Подключение к БД
database = Database(DATABASE_URL)
engine = create_engine(
    DATABASE_URL, echo=True
)

SessionLocal=sessionmaker(bind=engine)