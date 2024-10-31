from sqlalchemy import case
from datetime import datetime
from copy import deepcopy
from models import Todos, session

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

    my_todo_list = deepcopy(todo_list)

    if my_todo_list:
        # format the creation And due date
        for todo in my_todo_list:
            todo.creation_date = todo.creation_date.strftime('%a-%d-%b.')
            if todo.due_date:
                todo.due_date = todo.due_date.strftime('%a-%d-%b.')
    else:
        #If there is no todos, create one
        create_todo("My First ToDo", "Low", '')
        return get_all_todos()

    return my_todo_list

if __name__ == '__main__':
    for todo in get_all_todos():
        print(todo)