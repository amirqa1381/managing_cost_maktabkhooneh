from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


sql_alchemy_db_url = "sqlite:///./sqlite.db"


# for creating the engine of the database
engine = create_engine(sql_alchemy_db_url, connect_args={"check_same_thread": False})

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
        
        
    