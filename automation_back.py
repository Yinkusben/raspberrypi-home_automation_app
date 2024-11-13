from models import Device, session
import RPi.GPIO as GPIO
from gpiozero import LED, PWMLED

# Device set_up and control section

def setup_devices():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    for device in get_all_device():
        print(f"Initializing device: {device.device_name}")

        global PWM_instances
        PWM_instances = {}

        if device.type in ['LED', 'PWM']: #Check if device is a PWM device and create a PWM instance
            GPIO.setup(device.gpio_pin, GPIO.OUT)
            pwm_instance = GPIO.PWM(device.gpio_pin, 1000)
            pwm_instance.start(device.state)
            PWM_instances[device.id] = pwm_instance

        elif device.type in ['Switch', 'Relay']: #Initialize device to state
            GPIO.setup(device.gpio_pin, GPIO.OUT)
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

def control_device(device_id, value=0, toggle=False):
    if value in ['ON', 'on' '1', 1, True]:
        state = 1
    elif value in ['OFF', 'off', '0', 0, False]:
        state = 0
    else:
        state = int(value)

    device = session.query(Device).get(device_id)
    if device:
        if device.type in ['Switch', 'Relay']:
            GPIO.output(device.gpio_pin, state)

        elif device.type in ['LED', 'PWM']:
            if toggle:
                if device.id in PWM_instances:
                    PWM_instances[device.id].stop()
                    del PWM_instances[device.id]
                    print(f"Stop PWM, Writing {state}")
                    GPIO.output(device.gpio_pin, state)
                else:
                    print(f"writing {state}")
                    GPIO.output(device.gpio_pin, state)
            else:
                if device_id in PWM_instances: #Change PWM dutycylcle
                    print("wrong")
                    PWM_instances[device_id].ChangeDutyCycle(state)
                else:   #If PWM instance does not exist, Create it
                    print("wrong 2")
                    GPIO.setup(device.gpio_pin, GPIO.OUT)
                    pwm_instance = GPIO.PWM(device.gpio_pin, 1000)
                    pwm_instance.start(state)
                    PWM_instances[device.id] = pwm_instance

        device.state = state
        session.commit()
        return True
    
    return False

if __name__ == '__main__':
    for device in get_all_device():
        print(device)
    setup_devices()