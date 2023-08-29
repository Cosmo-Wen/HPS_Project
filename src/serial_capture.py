import serial
import time
# terminal:　python3 -m serial.tools.miniterm /dev/ttyUSB0 115200

class UWB3000Serial(serial.Serial):
    def __init__(self, path, baudrate):
        super().__init__(path, baudrate)
    
    def read_distance(self):
        """Returns the distance of 2 tags in meters.
        """
        self.write(b"Read Distance!\n")
        text = self.readline().decode('ascii')
        return float(text)
