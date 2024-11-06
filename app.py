from flask import Flask, render_template, redirect, url_for, request, jsonify
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
    default_state = request.form.get('default_state')

    automation.create_device(board=board, name=device_name, type=device_type, gpio_pin=GPIO_pin)
    return redirect(url_for('index'))

# Route to toggle a device state (ON/OFF)
@app.route('/toggle_device/<int:device_id>', methods=['POST'])
def toggle_device(device_id):
    print('toggling')
    if automation.control_device(device_id, toggle=True):
        return jsonify({"status": "success", "new_state": automation.get_device(device_id).state})
    
    return jsonify({"status": "error", "message": "Device not found"}), 404

# Route to adjust device brightness or PWM value
@app.route('/adjust_brightness/<int:device_id>', methods=['POST'])
def adjust_brightness(device_id):
    brightness = request.form.get('brightness')
    if automation.control_device(device_id=device_id, value=brightness, PWM=True):
        return jsonify({"status": "success", "brightness": device.brightness})
    return jsonify({"status": "error", "message": "Device not found or invalid brightness"}), 404

# Route to fetch sensor data (for display purposes)
# @app.route('/fetch_sensor_data/<int:device_id>', methods=['GET'])
# def fetch_sensor_data(device_id):
#     device = session.query(Devices).get(device_id)
#     if device and device.type in ["Temp sensor", "Humidity sensor", "Current sensor", "Voltage sensor"]:
#         # Fetch and return sensor reading (value stored in the database or fetched in real-time)
#         return jsonify({"status": "success", "reading": device.reading, "unit": device.unit})
#     return jsonify({"status": "error", "message": "Sensor not found or invalid device type"}), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)