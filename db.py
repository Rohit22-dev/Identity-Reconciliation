import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from threading import Lock
from models import Base

# Load environment variables
load_dotenv()

class Database:
    _instance = None
    _lock = Lock()

    def __new__(cls, connection_string: str):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Database, cls).__new__(cls)
                    cls._instance._initialize(connection_string)
        return cls._instance

    def _initialize(self, connection_string: str):
        self.engine = create_engine(connection_string, echo=True, pool_pre_ping=True)
        self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
        self.session_factory = scoped_session(self.SessionLocal)
        
        # Create tables if they don't exist
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()
    
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

# Initialize the database
connection_string = os.getenv("DB_CONNECTION_STRING")
database = Database(connection_string)

def get_db_session():
    db = database.get_session()
    try:
        yield db
    finally:
        db.close()
