from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DataBaseHandeler:
    _engine = None
    _session = None

    @staticmethod
    def setup():
        DataBaseHandeler.get_connection()
        DataBaseHandeler.get_session()

    @staticmethod
    def get_connection():
        if DataBaseHandeler._engine:
            return DataBaseHandeler._engine

        DataBaseHandeler._engine = create_engine('sqlite:///information.db')
        return DataBaseHandeler._engine

    @staticmethod
    def get_session():
        if DataBaseHandeler._session:
            return DataBaseHandeler._session

        Session = sessionmaker(bind=DataBaseHandeler.get_connection())
        DataBaseHandeler._session = Session()
        return DataBaseHandeler._session
