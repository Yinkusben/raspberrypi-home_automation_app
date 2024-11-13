from models import Device, session
from gpiozero import LED, PWMLED

# Device set_up and control section
def setup_devices():
    global LED_devices
    LED_devices = {}

    for device in get_all_device():
        print(f"Initializing device: {device.device_name}")

        if device.type == 'LED': #Check if device is a PWM device and create a PWM instance
            LED_device = PWMLED(device.gpio_pin)
            LED_devices[device.id] = LED_device
            control_device(device.id, device.state)

        # if device.type in ['Switch', 'Relay']: #Initialize device to state
        #     GPIO.setup(device.gpio_pin, GPIO.OUT)
        #     control_device(device_id=device.id, value=device.state)

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
        if device.type == 'LED':
            LED_devices[device.id].close()
            del LED_devices[device.id]

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
         create_device(board='Raspberry_pi', name='LED_1', type='LED', gpio_pin=17)
         return get_all_device()
     
     return devices

def control_device(device_id, value):
    if value in ['ON', 'on' '1', 1, True]:
        state = 1
    elif value in ['OFF', 'off', '0', 0, False]:
        state = 0
    else:
        state = int(value)

    device = session.query(Device).get(device_id)

    if device:
        if device.type == 'LED':
            if device.id not in LED_devices:
                #Add the instance of the LED to the dictionary
                LED_device = PWMLED(device.gpio_pin)
                LED_devices[device.id] = LED_device

            LED_device = LED_devices[device.id]

            if state > 1:
                val = (state/100) * 1.0 
                LED_device.value = val
            else:
                LED_device.on() if state == 1 else LED_device.off()

        device.state = state
        session.commit()
        return True
    
    return False

def cleanup():
    if LED_devices:
        for device in LED_devices:
            LED_devices[device].close()

if __name__ == '__main__':
    for device in get_all_device():
        print(device)
    setup_devices()