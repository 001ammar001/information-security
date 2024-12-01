import hashlib
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

    @staticmethod
    def create_user(user: "User"):
        salt = "5gz"
        salted_password = user.password + salt
        hashed = hashlib.md5(salted_password.encode())
        
        user.password = hashed.hexdigest()
        DataBaseHandeler.get_session().add(user)
        DataBaseHandeler.get_session().commit()


Base.metadata.create_all(DataBaseHandeler.get_connection())
