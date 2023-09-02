"""This module defines a class for interacting with a UWB 3000 Serial device.

Typical usage:
ser = UWB3000Serial(/tty/....)
"""

import time
import serial

class UWB3000Serial(serial.Serial):
    """Provides methods for working with a UWB 3000 Serial device.

    The 'UWB3000Serial' class extends 'serial.Serial' and communicates with
    a UBE3000 Serial device and retrieves distance data.

    Attributes: None
    """

    def __init__(self, path: str, baudrate: int) -> None:
        """Initialize the Serial device by calling the parent constructor.

        Args: 
            path: the serial device connected path
            baudrate: the transfer rate of the 

        Returns: None

        Raises: None
        """

        super().__init__(path, baudrate)
    
    def read_distance(self):
        """Reads and returns the distance of 2 tags  from the UWB device.

        Args: None

        Returns:
            float: The distance between the two tags in meters.
        
        Raises: None
        """

        self.write(b"Read Distance!\n")
        text = self.readline().decode('ascii')
        
        return float(text)
