from sqlalchemy import create_engine, Column, Integer, String, DateTime, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
import os

# Define the path to the database file
db_dir = os.path.join(os.path.dirname(__file__), '..', 'db')
db_path = os.path.join(db_dir, 'automate.db')

# Ensure the db directory exists
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

# Create the SQLAlchemy engine
engine = create_engine(f'sqlite:///{db_path}')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class LLMApi(Base):
    __tablename__ = 'llm_apis'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    _api_key = Column(String, nullable=False)
    # TODO: handle this securely before ship to production
    base_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    last_used_at = Column(DateTime, nullable=True)
    is_active = Column(Integer, default=True)
    

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(TEXT)
    workspace_dir = Column(String, nullable=False)  # Directory where task files are stored
    code_entry_point = Column(String, nullable=False)  # Main file to execute
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    last_run_at = Column(DateTime, default=None)
    interval = Column(Integer, nullable=False)  # Interval in minutes
    status = Column(String, default="idle")  # [success, idle, failed]
    is_attached = Column(Integer, default=True) 
    # True = task is in evaluation, False = task is ready to be runned by user
    log_file = Column(String, nullable=True)  # Path to the task log file

Base.metadata.create_all(engine)