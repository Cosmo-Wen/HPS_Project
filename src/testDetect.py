import asyncio 

from time import sleep, time

class Lid:
    def __init__(self):
        self._flag = False
        self._sense_event = asyncio.Event()
        self._sense_event.clear()
    
    def turn_on(self):
        self._sense_event.set()
    
    def turn_off(self):
        self._sense_event.clear()
    
    def shutdown(self):
        print('detect shutdown')

    async def sense(self):
        while True:
            await self._sense_event.wait()
            print('Detecting...')
            await asyncio.sleep(1)
