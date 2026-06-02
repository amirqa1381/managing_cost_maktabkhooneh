import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

sql_alchemy_db_url = os.getenv("DATABASE_URL")
if not sql_alchemy_db_url:
    raise RuntimeError("DATABASE_URL is not set")

connect_args = (
    {"check_same_thread": False}
    if sql_alchemy_db_url.startswith("sqlite")
    else {}
)


# for creating the engine of the database
engine = create_engine(sql_alchemy_db_url, connect_args=connect_args)

# creating the session for keep connection between the DB and client
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# create base class for declaring tables
Base = declarative_base()


def get_db():
    db = session_local()
    try:
        yield db

    finally:
        db.close()
