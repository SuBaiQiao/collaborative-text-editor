from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# 存储文本历史记录的列表
text_history = []


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('text_update')
def handle_text_update(data):
    # 更新文本并将其添加到历史记录中
    new_text = data['text']
    if new_text != (text_history[-1] if text_history else ""):
        text_history.append(new_text)
        socketio.emit('text_update', {'text': new_text})  # 广播新文本


@socketio.on('get_current_text')
def handle_get_current_text():
    # 发送当前文本内容（可以根据需要调整）
    current_text = text_history[-1] if text_history else ""
    socketio.emit('text_update', {'text': current_text})


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
