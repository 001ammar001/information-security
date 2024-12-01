from sqlalchemy import Column, Integer, String, Double
from sqlalchemy.ext.declarative import declarative_base
from database import DataBaseHandeler

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    balance = Column(Double, nullable=False)

Base.metadata.create_all(DataBaseHandeler.get_connection())