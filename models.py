import hashlib
from sqlalchemy import Column, Integer, String, Double
from sqlalchemy.ext.declarative import declarative_base

from database import DataBaseHandeler

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    balance = Column(Double, nullable=False)

    @staticmethod
    def _check_user_name_uniquenes(session, user_name):
        user = session.query(User).filter_by(user_name=user_name).first()
        if (user):
            raise ValueError

    @staticmethod
    def create_user(user: "User"):
        salt = "5gz"
        salted_password = user.password + salt
        hashed = hashlib.md5(salted_password.encode())
        user.password = hashed.hexdigest()
        session = DataBaseHandeler.get_session()
        try:
            User._check_user_name_uniquenes(
                session=session, user_name=user.user_name
            )
        except ValueError:
            return "User alread exists"

        session.add(user)
        session.commit()

        return "user created sucsessfully"

    @staticmethod
    def get_user(user_name: str, password: str) -> "User":
        session = DataBaseHandeler.get_session()
        user = session.query(User).filter_by(user_name=user_name).first()
        return user


Base.metadata.create_all(DataBaseHandeler.get_connection())
