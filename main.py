import asyncio
from src.move import move
from src.enums import Instructions, States, Actions
from src.user_interface import fetch_instructions
from src.control import Lid # Control Module
# from src.testDetect import Lid # Ideal Result

async def process_instruction(instruction: Instructions = Instructions.INVALID, state: States = States.INVALID, user_interface = None):
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
            # user_interface.reject_instruction(message = 'Invalid instruction')
            print('Invalid instruction')
        elif instruction == Instructions.START:
            print('Starting...')
            await asyncio.sleep(5)
            print('Started')
        else: 
            # user_interface.reject_instruction(message = 'Currently turned off.')
            print('Currently turned off.')
    elif state == States.ONLINE:
        if instruction ==  Instructions.START: 
            # user_interface.reject_instruction(message = 'Already started.')
            print('Already started.')
        elif instruction ==  Instructions.END: 
            print('Ending...')
            await asyncio.sleep(2)
            status = Actions.HALT
        elif instruction ==  Instructions.MOVE:
            await move()
        elif instruction ==  Instructions.RETURN:
            print('Start moving...')
            await asyncio.sleep(2)
            print('End moving')
        elif instruction ==  Instructions.INVALID:
            # user_interface.reject_instruction(message = 'Invalid instruction')
            print('Invalid instruction')
        else:
            # user_interface.reject_instruction(message = 'Invalid instruction')
            print('Invalid instruction')
    
    return status

async def instruction_consumer(queue: asyncio.Queue, user_interface = None, lid = None) -> None:
    """ Retrieve instruction from the queue and call relevant processing methods

    Asynchronously retrieve instructions from the queue
    Processes instruction and depending on the instruction, clear the queue
    
    Warning: If more than two threads, be careful for race conditions and multiple clears

    Args:
        queue: instruction queue
    
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
            print(f'Queue contents: {list(queue._queue)}')
            continue
        
        result = await process_instruction(instruction, state) # user_interface
        if result == Actions.HALT:
            print("Clearing the queue...")
            queue._queue.clear()
            print('Ended')
        
        queue.task_done() 
        if state == States.ONLINE and queue.empty() and result != Actions.HALT:
            lid.turn_on()
            
        # user_interface.log_reply(f'Processed Instruction: {instruction}, {len(queue._queue)} remaining.')
        print(f'Processed Instruction: {instruction}, {len(queue._queue)} remaining.')

async def main():
    try:
        instruction_queue = asyncio.Queue()
        # user_interface = LineAPI()
        lid_control = Lid()

        # Instruction Queue
        instruction_queue_task = asyncio.create_task(instruction_consumer(instruction_queue, lid = lid_control))
        # Human Detection
        detection_task = asyncio.create_task(lid_control.sense())

        shutdown = False
        state = States.IDLE

        while not shutdown:
            instruction: Instructions = await fetch_instructions()
            await instruction_queue.put((instruction, state))
            # user_interface.send_message(f'Added instruction: {instruction}, {len(instruction_queue._queue)} in line.')
            print(f'Added instruction: {instruction}, {len(instruction_queue._queue)} in line.')
            if instruction == Instructions.SHUTDOWN:
                shutdown = True
            elif state == States.IDLE and instruction == Instructions.START:
                state = States.ONLINE
                lid_control.turn_on()
            elif state == States.ONLINE and instruction == Instructions.END:
                state = States.IDLE
                lid_control.turn_off()
        
        await instruction_queue.join()

        await instruction_queue.put(None)
        await instruction_queue_task
        await detection_task
    finally:
        lid_control.shutdown()

if __name__ == '__main__':
    asyncio.run(main())
