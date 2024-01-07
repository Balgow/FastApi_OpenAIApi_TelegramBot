from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

DATABASE_URL = os.environ.get('DATABASE_URL')

engine = create_engine(DATABASE_URL, connect_args={"options": "-csearch_path=email_service"})
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind = engine)
Base = declarative_base()