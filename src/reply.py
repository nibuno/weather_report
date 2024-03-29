# coding: utf-8
"""LineBotの応答メッセージ"""
import os

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from weather_report import weather_report, weather_report_telop, weather_link

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ['YOUR_CHANNEL_ACCESS_TOKEN']
YOUR_CHANNEL_SECRET = os.environ['YOUR_CHANNEL_SECRET']

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route('/callback', methods=['POST'])
def callback():
    """ webhookURLが叩かれた際に実行される"""
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print('Invalid signature. '
              'Please check your channel access token/channel secret.')
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """ LINEBotの応答メッセージを返却する"""
    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(text=weather_report(is_local_debug=False)),
         TextSendMessage(text=weather_report_telop(is_local_debug=False)),
         TextSendMessage(text=weather_link(is_local_debug=False))]
    )


if __name__ == '__main__':
    # herokuのデプロイのためポート番号を指定
    port = int(os.getenv('PORT', '5000'))
    app.run(host='0.0.0.0', port=port)
