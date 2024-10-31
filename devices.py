from models import Device, session

#Create a device
def create_device(board, name, type, gpio_pin, default_state):
    new_device = Device(
        board = board,
        device_name = name,
        type = type,
        gpio_pin = gpio_pin,
        default_state = default_state
    )

    session.add(new_device)
    session.commit()

def delete_device(device_id):
    device = session.query(Device).filter_by(id=device_id).first()
    if device:
        session.delete(device)
        session.commit()

def get_all_device():
     devices = session.query(Device).all()

     #If there are no device create one
     if not devices:
         create_device(board='Raspberry_pi', name='LED_1', type='LED', gpio_pin=11, default_state=0)
         return get_all_device()
     
     return devices

if __name__ == '__main__':
    for device in get_all_device():
        print(device)