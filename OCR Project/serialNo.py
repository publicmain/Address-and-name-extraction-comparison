import datetime
import random

def get_serialNo():
    now = datetime.datetime.now()
    serial_number = now.strftime('%Y%m%d%H%M') + f"{now.microsecond // 100:04d}"
    random_number = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    serial_number_with_random = serial_number + random_number
    return serial_number_with_random
