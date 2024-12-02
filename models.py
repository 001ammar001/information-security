from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import hashlib
import json
import os
from dotenv import load_dotenv
from symmetric_crypt import encrypt,decrypt
from database import DataBaseHandeler

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    balance = Column(String, nullable=False)

    @staticmethod
    def _check_user_name_uniquenes(session, user_name) -> None:
        user = session.query(User).filter_by(user_name=user_name).first()
        if (user):
            raise ValueError

    @staticmethod
    def _hash_password(password) -> str:
        salt = "5gz"
        salted_password = password + salt
        hashed = hashlib.md5(salted_password.encode())
        return hashed.hexdigest()
    
    @staticmethod
    def get_username(id):
        session = DataBaseHandeler.get_session()
        user = session.query(User).filter_by(user_id=id).first()
        return user.user_name 
    
    @staticmethod
    def create_user(user: "User"):
        user.password = User._hash_password(password=user.password)
        session = DataBaseHandeler.get_session()

        try:
            User._check_user_name_uniquenes(
                session=session, user_name=user.user_name
            )
        except ValueError:
            return json.dumps(
                {'status': "error", 'message': "Username has already been taken"}
            )

        session.add(user)
        session.commit()
        return json.dumps(
            {'status': "success", 'message': "User created successfully"}
        )

    @staticmethod
    def login(user_name: str, password: str):
        session = DataBaseHandeler.get_session()
        user = session.query(User).filter_by(user_name=user_name).first()

        if (not user or User._hash_password(password) != user.password):
            return json.dumps(
                {'status': "error", 'message': "User does not exists"}
            )

        return json.dumps(
            {'status': "success", 'message': "user login successfully","server_key": os.environ.get("RSA_PUBLIC_KEY")}
        )

    @staticmethod
    def deposit(user_id, amount):
        session = DataBaseHandeler.get_session()
        user = session.query(User).filter_by(user_id=user_id).first()
        print(user.balance)
        old_balance = decrypt(key=os.environ.get("AES_KEY").encode(),message=user.balance)
        user.balance = encrypt(key=os.environ.get("AES_KEY").encode(),message=(str(float(amount) + float(old_balance))).encode())
        new_balance = decrypt(key=os.environ.get("AES_KEY").encode(),message=user.balance)
        session.commit()
        return json.dumps(
            {'status': "success", 'message': f"balance update successfully {new_balance}"}
        )

    @staticmethod
    def withdraw(user_id, amount):
        session = DataBaseHandeler.get_session()
        user = session.query(User).filter_by(user_id=user_id).first()
        # TODO: we need to decrypt the value before doing the calculation
        if (float(user.balance) >= float(amount)):
            user.balance = str(float(user.balance) - float(amount))
            session.commit()
            return json.dumps(
                {'status': "success",
                    'message': f"balance update successfully {user.balance}"}
            )

        return json.dumps(
            {'status': "error", 'message': f"insufficient balance {user.balance}"}
        )

    @staticmethod
    def get_balance(user_id: int):
        session = DataBaseHandeler.get_session()
        user = session.query(User).filter_by(user_id=user_id).first()

        if (not user):
            return json.dumps(
                {'status': "error", 'message': "User does not exists"}
            )

        return json.dumps(
            {'status': "success", 'message': f"your balance is {user.balance}"}
        )


    

Base.metadata.create_all(DataBaseHandeler.get_connection())

if __name__ == "__main__":
    load_dotenv()
    User.deposit(1,100)