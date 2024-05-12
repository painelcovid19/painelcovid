from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
# from config import DevelopmentConfig
import os 

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")



dialect = "oracle"
driver = "oracledb"
username = "DEMBO"
password = ""
port = os.environ.get("DB_PORT")
host = DB_HOST
database = "desafio_ascan"
dsn = ""
connection_string = f"{dialect}+{driver}://{username}:{password}@{dsn}"

class DBConnectionHandler:
    
    def __init__(self) -> None:
        self.__conection_string = connection_string
        self.__engine = self.__create_engine()
        self.session = None
        
    def __create_engine(self):
        engine = create_engine(self.__conection_string, echo=False)
        return engine
    
    def get_engine(self):
        return self.__engine
    
    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        self.session = session_make()
        return self
    
    def __exit__(self, exc_type, exp_val, exc_tb):
        self.session.close()
        
if __name__ == "__main__":
    db = DBConnectionHandler()