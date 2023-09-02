""" This module take cares of the user input and turns it into intructions

The fetch_intrusction() retrieves the instruction and the other two logs or
warns the user of incorrect usage.

Typical usage:
await intruction = fetch_intructions()
if instruction is ...
    log_reply(...)/reject_instruction(...)
"""

import asyncio

from .header import Instructions

async def fetch_instructions() -> Instructions:
    """Temporary input method

    Takes an terminal input and returns the instruction type depending on the input

    Args: None

    Returns: 
        instruction: Specific instruction type
    
    Raises: None
    """

    loop = asyncio.get_running_loop()
    user_input = await loop.run_in_executor(None, input, "Enter instruction: (Start, Move, End)")
    if user_input.lower() == 'start': instruction = Instructions.START
    elif user_input.lower() == 'end': instruction = Instructions.END
    elif user_input.lower() == 'move': instruction = Instructions.MOVE
    elif user_input.lower() == 'return': instruction = Instructions.RETURN
    elif user_input.lower() == 'log': instruction = Instructions.LOG
    elif user_input.lower() == 'is it full': instruction = Instructions.ISFULL
    else: instruction = Instructions.INVALID
    return instruction

def reject_instruction(message: str):
    """Logs error messages
    
    Args: 
        message: error message
    
    Returns: None

    Raises: None
    """

    print(f'Error: {message}.')

def log_reply(message: str):
    """Logs replying messages
    
    Args: 
        message: error message
    
    Returns: None

    Raises: None
    """

    print(f'Log: {message}')