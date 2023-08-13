from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 初始化全域變數，用來存儲最新的訊息內容
latest_message = ""

# 設定Channel Access Token和Channel Secret
line_bot_api = LineBotApi('Orj4xNTzu4lZEwnUuf5B1Sdez01KSPtyBo1UC1ZnpPS93AMguOYc4XkQuw1BqIIDdmgITw4guIGtkJJ98w/y3sUM3MqXFQoaXtpw4bzWVuB0fxdCa3a2sGzRVS2W+HqOJOHV8BIGzl3QQe3ygcw4hAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('551d866b1602853292a0c02b7ef8055c')

# 發送訊息並開始監聽的函式
def send_message_and_listen():
    send_message_to_user('Ua228ca9743237fb1fb497b4b3d0247c9', "已開始監聽聊天訊息")#User_id
    app.run()  # 開始伺服器運行
    return lastest_message  # 回傳最新的訊息內容

# 發送訊息的函式
def send_message(msg):
    send_message_to_user('Ua228ca9743237fb1fb497b4b3d0247c9', msg)
    return "已傳送" + msg

# 發送訊息給特定使用者的函式
def send_message_to_user(user_id, message_text):
    message = TextSendMessage(text=message_text)
    line_bot_api.push_message(user_id, messages=message)

# 處理 LINE 的 Webhook 訊息
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理文字訊息的事件
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global lastest_message  # 使用全域變數來儲存最新的訊息內容
    user_id = event.source.user_id# 這段可以解析出User_id然後放在第17行
    message_text = event.message.text
    lastest_message = message_text  # 更新最新的訊息內容
    shutdown_server()  # 呼叫自定義的結束函式

# 自定義的伺服器關閉函式
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug server')
    func()

if __name__ == "__main__":
    # 呼叫 send_message_and_listen() 函式，開始發送訊息並監聽
    target_1 = send_message_and_listen()
    print("開始監聽的訊息內容：", target_1)

    # 呼叫 send_message() 函式，發送 "hello" 訊息
    target_2 = send_message("hello")
    print("發送的訊息結果：", target_2)
