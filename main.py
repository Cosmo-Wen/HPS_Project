import asyncio

from src.enums import Instructions, States, Actions
from LineAPI import LineAPI, fetch_instructions


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
            user_interface.reject_instruction(message = 'Invalid instruction')
        elif instruction == Instructions.START:
            print('Starting...')
            await asyncio.sleep(2)
            print('Started')
        else: 
            user_interface.reject_instruction(message = 'Currently turned off.')
    
    elif state == States.ONLINE:
        match instruction:
            case Instructions.START: 
                user_interface.reject_instruction(message = 'Already started.')
            case Instructions.END: 
                print('Ending...')
                await asyncio.sleep(2)
                status = Actions.HALT
            case Instructions.MOVE:
                print('Start moving...')
                await asyncio.sleep(2)
                print('End moving')
            case Instructions.RETURN:
                print('Start moving...')
                await asyncio.sleep(2)
                print('End moving')
            case Instructions.INVALID:
                user_interface.reject_instruction(message = 'Invalid instruction')
            case _:
                user_interface.reject_instruction(message = 'Invalid instruction')
    
    return status

async def instruction_consumer(queue: asyncio.Queue, user_interface) -> None:
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
        instruction, state = await queue.get()

        if instruction == Instructions.LOG:
            print(f'Queue contents: {list(queue._queue)}')
            continue

        result = await process_instruction(instruction, state, user_interface)
        if result == Actions.HALT:
            print("Clearing the queue...")
            queue._queue.clear()
            print('Ended')
        queue.task_done()
        user_interface.log_reply(f'Processed Instruction: {instruction}, {len(queue._queue)} remaining.')

async def main():
    instruction_queue = asyncio.Queue()
    user_interface = LineAPI()

    # Instruction Queue
    instruction_queue_task = asyncio.create_task(instruction_consumer(instruction_queue))
    # Human Detection
    detection_task = asyncio.create_task()
   
    state = States.IDLE

    while True:
        instruction: Instructions = await fetch_instructions()
        await instruction_queue.put((instruction, state))
        user_interface.send_message(f'Added instruction: {instruction}, {len(instruction_queue._queue)} in line.')

        if state == States.IDLE and instruction == Instructions.START:
            state = States.ONLINE
        elif state == States.ONLINE and instruction == Instructions.END:
            state = States.IDLE

    await instruction_queue.join()

    await instruction_queue.put(None)
    await consumer_task

if __name__ == '__main__':
    asyncio.run(main())
