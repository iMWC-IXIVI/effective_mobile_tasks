import os

from pathlib import Path

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


load_dotenv()

SRC_PATH = Path('./files')
URL = 'https://spimex.com/markets/oil_products/trades/results/'

DB_URL = os.getenv('DB_URL')
engine = create_engine(url=DB_URL)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
