from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Create the SQLAlchemy engine
DATABASE_URL = 'sqlite:///database.db'
engine = create_engine(DATABASE_URL, echo=False)

# Base class for declarative models
Base = declarative_base()

class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    status = Column(String, default="Not-started")
    creation_date = Column(Date, default=datetime.now())
    due_date = Column(Date, nullable=True)

    def __repr__(self):
        return f"<Todos(title={self.title}, priority={self.priority}, status={self.status})>"

class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    board = Column(String, nullable=False)
    device_name = Column(String, nullable=False, unique=True)
    type = Column(String, nullable=False)
    gpio_pin = Column(Integer, nullable=False)
    state = Column(Integer)

    def __repr__(self):
        return f"<Device name={self.device_name}, type={self.type}, GPIO_pin={self.gpio_pin}, state={self.state}>"
    
# Initialize the database (create tables)
Base.metadata.create_all(engine)

# SQLAlchemy session setup
Session = sessionmaker(bind=engine)
session = Session()