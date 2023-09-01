import serial
import time
# terminal:　python3 -m serial.tools.miniterm /dev/ttyUSB0 115200

class UWB3000Serial(serial.Serial):
    def __init__(self, path, baudrate):
        super().__init__(path, baudrate)
    
    def read_distance(self):
        """Returns the distance of 2 tags in meters.
        """
        print('stest1')
        self.write(b"Read Distance!\n")
        print('stest2')
        text = self.readline().decode('ascii')
        print('stest3')
        return float(text)
