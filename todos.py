from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, case
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from copy import deepcopy

# Create the SQLAlchemy engine
DATABASE_URL = 'sqlite:///todos.db'
engine = create_engine(DATABASE_URL, echo=False)

# Base class for declarative models
Base = declarative_base()

# SQLAlchemy session setup
Session = sessionmaker(bind=engine)
session = Session()

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

# Initialize the database (create tables)
def initialize():
    Base.metadata.create_all(engine)

# Create a new todo
def create_todo(title, priority, due_date):
    new_todo = Todos(
        title=title,
        priority=priority,
        status='Not-started',
        creation_date=datetime.now(),
        due_date=datetime.strptime(due_date, '%Y-%m-%d') if due_date else None
    )
    
    session.add(new_todo)
    session.commit()

# Update a todo
def update_todo(todo_id, priority, status, due_date):
    todo = session.query(Todos).filter_by(id=todo_id).first()
    if todo:
        todo.priority = priority
        todo.status = status
        todo.due_date = datetime.now()
        todo.due_date = datetime.strptime(due_date, '%Y-%m-%d') if due_date else None
        session.commit()

# Delete a todo
def delete_todo_by_id(todo_id):
    todo = session.query(Todos).filter_by(id=todo_id).first()
    if todo:
        session.delete(todo)
        session.commit()

# Get all todos
def get_all_todos():
    todo_list = session.query(Todos).order_by(
        case(
            (Todos.priority == 'High', 1),
            (Todos.priority == 'Mid', 2),
            (Todos.priority == 'Low', 3)
        ).asc()
    ).all()

    if todo_list:
        my_todo_list = deepcopy(todo_list)

        for todo in my_todo_list:  # format the creation And due date
            todo.creation_date = todo.creation_date.strftime('%a-%d-%b.')
            if todo.due_date:   #Check if there's due date and format it
                todo.due_date = todo.due_date.strftime('%a-%d-%b.')

    return my_todo_list

if __name__ == '__main__':
    initialize()
    create_todo("My first todo item", "Low", '2024-10-10')

    # for todo in get_all_todos():
    #     print(type(todo.creation_date))
    # delete_todo_by_id(3)