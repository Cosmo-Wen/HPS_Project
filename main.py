""" X-trash: More time for you, less for trashing.

This script executes the program for running X-trash.

Usage example:
$ python main.py
"""

import asyncio

import RPi.GPIO as GPIO

from src.control import Lid # Control Module
from src.header import Instructions, States, Actions
from src.move import Move
from src.user_interface import *

class Main:
    """ This is the program class that runs when the script is executed.

    This class creates coroutines and runs the UI, process, and lid control
    through these separately.

    Attributes:
        move: A movement method object
    """

    def __init__(self) -> None:
        """ Set up internal attributes.

        Args: None
        """

        GPIO.setmode(GPIO.BCM)
        self._move = Move()

    async def process_instruction(
        self, instruction: Instructions = Instructions.INVALID, 
        state: States = States.INVALID
    ) -> None:
        """ Processes the current instruction depending on the state

        Retrieve the instruction and the state
        Processes and logs the relevant actions

        Args:
            instruction: the current received instruction
            state: the state when the instruction is received
        
        Returns:
            status: an action regarding whether the state should be changed

        Raises: None
        """

        status = Actions.NOTHING

        if state == States.IDLE:
            if instruction == Instructions.INVALID:
                reject_instruction('Invalid instruction')
            elif instruction == Instructions.START:
                log_reply('Starting...')
                await asyncio.sleep(5)
                log_reply('Started')
            else: 
                reject_instruction('Currently turned off.')
        elif state == States.ONLINE:
            if instruction ==  Instructions.START: 
                reject_instruction('Already started.')
            elif instruction ==  Instructions.END: 
                log_reply('Ending...')
                await asyncio.sleep(2)
                status = Actions.HALT
            elif instruction ==  Instructions.MOVE:
                await self._move.move()
            elif instruction ==  Instructions.RETURN:
                log_reply('Start moving...')
                await asyncio.sleep(2)
                log_reply('End moving')
            elif instruction ==  Instructions.INVALID:
                reject_instruction('Invalid instruction')
            else:
                reject_instruction('Invalid instruction')
        
        return status

    async def instruction_consumer(
        self, queue: asyncio.Queue, 
        lid = None
    ) -> None:
        """ Retrieve instruction from the queue and call processing methods

        Asynchronously retrieve instructions from the queue
        Processes instruction and depending on the instruction, clear the queue
        
        Warning: If more than two threads, be careful for race conditions and 
        multiple clears

        Args:
            queue: instruction queue
            lid: lid control object
        
        Returns: None

        Raises: None
        """

        while True:
            item = await queue.get()
            if item is None:
                break
            instruction, state = item
            if state == States.ONLINE:
                lid.turn_off()
            if instruction == Instructions.LOG:
                log_reply(f'Queue contents: {list(queue._queue)}')
                continue
            
            result = await self.process_instruction(instruction, state)
            if result == Actions.HALT:
                log_reply("Clearing the queue...")
                queue._queue.clear()
                log_reply('Ended')
            
            queue.task_done() 
            if (
                state == States.ONLINE 
                and queue.empty() 
                and result != Actions.HALT
            ):
                lid.turn_on()
                
            log_reply((f'Processed Instruction: {instruction},' 
                       '{len(queue._queue)} remaining.'))
    
    def shutdown(self) -> None:
        """ Clean GPIO, PWM, and Robot instances.

        lid_control has GPIO and PWM instances
        move has GPIO and robot instances

        Args: None

        Returns: None

        Raises: None
        """

        GPIO.cleanup()
        self._move.shutdown()

    async def run(self) -> None:
        """ The main script that runs when the program is executed.

        It mainly consists of a while loop that runs until forcibly 
        turned off, which will trigger the finally and do proper shutdown
        routines.

        Args: None

        Returns: None

        Raises: None
        """
        
        try:
            instruction_queue = asyncio.Queue()
            lid_control = Lid()
            # user_interface = LineAPI()

            # Instruction Queue
            instruction_queue_task = asyncio.create_task(
                self.instruction_consumer(instruction_queue, lid = lid_control)
            )
            # Human Detection
            detection_task = asyncio.create_task(lid_control.sense())

            shutdown = False
            state = States.IDLE

            while not shutdown:
                instruction: Instructions = await fetch_instructions()
                await instruction_queue.put((instruction, state))
                log_reply((f'Added instruction: {instruction},' 
                           '{len(instruction_queue._queue)} in line.'))
                if state == States.IDLE and instruction == Instructions.START:
                    state = States.ONLINE
                    lid_control.turn_on()
                elif (
                    state == States.ONLINE 
                    and instruction == Instructions.END
                ):
                    state = States.IDLE
                    lid_control.turn_off()
            
            await instruction_queue.join()

            await instruction_queue.put(None)
            await instruction_queue_task
            await detection_task
        finally:
            self.shutdown()

if __name__ == '__main__':
    main = Main()
    asyncio.run(main.run())
