import asyncio

from .enums import Instructions

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

class LineAPI:
    def __init__(self):
        self._app = Flask(__name__)
        self._api = LineBotApi('Orj4xNTzu4lZEwnUuf5B1Sdez01KSPtyBo1UC1ZnpPS93AMguOYc4XkQuw1BqIIDdmgITw4guIGtkJJ98w/y3sUM3MqXFQoaXtpw4bzWVuB0fxdCa3a2sGzRVS2W+HqOJOHV8BIGzl3QQe3ygcw4hAdB04t89/1O/w1cDnyilFU=')
        self._handler = WebhookHandler('551d866b1602853292a0c02b7ef8055c')
        self._current_user = 'Ua228ca9743237fb1fb497b4b3d0247c9'
        self.init_routes()
        self._latest_message=''
    
    def init_routes(self):
        @self._app.route("/callback", methods=['POST'])
        def callback():
            signature = request.headers['X-Line-Signature']
            body = request.get_data(as_text=True)
            try:
                self._handler.handle(body, signature)
            except InvalidSignatureError:
                abort(400)
            return 'OK'

        @self._handler.add(MessageEvent, message=TextMessage)
        def handle_message(event):
            self._lastest_message = event.message.text  # 更新最新的訊息內容
            self.shutdown_server()  # 呼叫自定義的結束函式
    
    async def listen(self):
        self._app.run(port=8000)
        return self._lastest_message
    
    def reject_instruction(self, message: str):
        """Logs error messages
        
        Args: 
            message: error message
        
        Returns: None

        Raises: None
        """
        text = TextSendMessage(text=message)
        self._api.push_message(self._current_user, messages=f'Error: {text}.')

    def log_reply(self, message: str):
        """Logs replying messages
        
        Args: 
            message: error message
        
        Returns: None

        Raises: None
        """
        text = TextSendMessage(text=message)
        self._api.push_message(self._current_user, f'Log: {message}')

    def shutdown_server(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug server')
        func()

async def fetch_instructions(user_interface) -> Instructions:
    """Temporary input method

    Takes an terminal input and returns the instruction type depending on the input

    Args: None

    Returns: 
        instruction: Specific instruction type
    
    Raises: None
    """
    loop = asyncio.get_running_loop()
    user_input = await user_interface.listen()
    match user_input:
        case 'start': instruction = Instructions.START
        case 'end': instruction = Instructions.END
        case 'move': instruction = Instructions.MOVE
        case 'return': instruction = Instructions.RETURN
        case 'log': instruction = Instructions.LOG
        case _: instruction = Instructions.INVALID
    return instruction