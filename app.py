from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_socketio import SocketIO, emit
from keys import weather_key, lat, lon, city, state
from gcalendar import Gcalendar
from weather import Weather
from datetime import datetime
import todos
import automation


# Weather
my_weather = Weather()
get_weather = my_weather.get_data(weather_key, lat, lon)

# Events
my_cal = Gcalendar()
get_events = my_cal.gcal_connect()

#Setup devices
automation.setup_devices()

# Today's date for header
def today_date():
    date = datetime.now()
    return date.strftime("%A, %B %d")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'home_server'
socketio = SocketIO(app)  # Initialize Flask-SocketIO

@app.route('/')
def index():
    # get all items from our DB
    tasks = todos.get_all_todos()
    my_devices = automation.get_all_device()

    # priority = ["High", "Mid", "Low"]
    # for task in tasks:
    #     task.priority = priority[task.priority]

    # handle getting today's date for the header
    return render_template(
        'index.html',
        date=today_date(),
        weather=get_weather,
        events=get_events,
        len_todo=len(tasks),
        todos=tasks,
        devices=my_devices
    )

@app.route('/save-todo-item', methods=['GET', 'POST'])
def save_todo():
    data = request.form.to_dict()
    print("Adding to todo:", data)
    
    todos.create_todo(data['title'], data['priority'], data['due_date'])
    return redirect(url_for('index'))

@app.route('/delete-todo/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    todos.delete_todo_by_id(todo_id)
    return redirect(url_for('index'))

@app.route('/update-todo/<int:todo_id>', methods=['POST']) #New one
def update_todo(todo_id):
    priority = request.form.get('priority')
    status = request.form.get('status')
    due_date = request.form.get('due_date')

    todos.update_todo(todo_id, priority, status, due_date)
    return redirect(url_for('index'))

@app.route('/add-device', methods=['POST'])
def add_device():
    board = request.form.get('board')
    device_name = request.form.get('device_name')
    device_type = request.form.get('device_type')
    GPIO_pin = request.form.get('gpio')

    automation.create_device(board=board, name=device_name, type=device_type, gpio_pin=GPIO_pin)
    return redirect(url_for('index'))

# Handle device ON/OFF control
@socketio.on('toggle_device')
def toggle_device(data):
    print('toggling')
    device_id = data.get('device_id')
    state = data.get('state')
    
    if automation.control_device(device_id, state):
        emit('device_state_updated', {'device_id': device_id, 'new_state': state}, broadcast=True)
    else:
        emit('device_state_updated', {'device_id': device_id, 'new_state': not state}, broadcast=True)

if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=8000)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)