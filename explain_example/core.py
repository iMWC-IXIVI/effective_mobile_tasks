import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from dotenv import load_dotenv


load_dotenv()


DB_URL = os.getenv('DB_URL')
engine = create_engine(url=DB_URL)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
