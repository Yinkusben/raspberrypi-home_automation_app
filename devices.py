from models import Device, session
import RPi.GPIO as GPIO
from gpiozero import LED, PWMLED

# Device set_up and control section

def setup_devices():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    for device in get_all_device():
        if device.type == 'DHT11':
            import time
            import adafruit_dht
            import board

            
        print(f"Initializing device: {device.device_name}")
        GPIO.setup(device.gpio_pin, GPIO.OUT)
        #Initialize device to state
        control_device(device_id=device.id, value=device.state)

#Create a device
def create_device(board, name, type, gpio_pin):
    new_device = Device(
        board = board,
        device_name = name,
        type = type,
        gpio_pin = gpio_pin,
        state = 0
    )

    session.add(new_device)
    session.commit()

#Function to delete a single device
def delete_device(device_id):
    device = session.query(Device).filter_by(id=device_id).first()
    if device:
        GPIO.cleanup(device.gpio_pin)
        session.delete(device)
        session.commit()
        return True
    return "Error, no such device"

#Function to get a single device
def get_device(device_id):
    device = session.query(Device).filter_by(id=device_id).first()
    if device:
        return device
    return f"device with id: {device_id} not found!"

#Function to get all devices
def get_all_device():
     devices = session.query(Device).all()

     #If there are no device create one
     if not devices:
         create_device(board='Raspberry_pi', name='LED_1', type='LED', gpio_pin=11)
         return get_all_device()
     
     return devices

def control_device(device_id, value=0, toggle=False, PWM=False):
    if value in ['ON', 'on' '1', 1, True]:
        state = 1
    elif value in ['OFF', 'off', '0', 0, False]:
        state = 0
    else:
        state = value

    device = session.query(Device).get(device_id)
    if device:
        if toggle:
            device.state = 1 if device.state == 0 else 0
            GPIO.output(device.gpio_pin, device.state)
            session.commit()
            return True

        if PWM:
            PWM_control = GPIO.PWM(device.gpio_pin, 500)
            PWM_control.start(state)
        else:
            GPIO.output(device.gpio_pin, state)

        device.state = state
        session.commit()
        return True
    
    return False

if __name__ == '__main__':
    for device in get_all_device():
        print(device)
    setup_devices()