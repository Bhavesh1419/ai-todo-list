from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite Database URL
DATABASE_URL = "sqlite:///./tasks.db"

# Create the database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session for database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define Base class for models
Base = declarative_base()

# Define Task Model
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    category = Column(String, default="TBD")

# Create the tables in the database
Base.metadata.create_all(bind=engine)
