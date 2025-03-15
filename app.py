from flask import Flask, render_template, request, send_file
from flask_socketio import SocketIO
import os

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 900
socketio = SocketIO(app, ping_timeout=900, ping_interval=300)

# 文件存储目录
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 存储文本历史记录的列表
text_history = []
file_list = []


def remove_all_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")


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


@socketio.on('file_list_update')
def handle_file_list_update():
    socketio.emit('file_list_update', {'file_list': file_list})


@socketio.on('get_current_text')
def handle_get_current_text():
    # 发送当前文本内容（可以根据需要调整）
    current_text = text_history[-1] if text_history else ""
    socketio.emit('text_update', {'text': current_text})


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        if file.filename in file_list:
            return 'File already exists', 400
        file_list.append(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        socketio.emit('file_list_update', {'file_list': file_list})
        return 'File uploaded successfully', 200


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        return 'File not found', 404
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    remove_all_files(UPLOAD_FOLDER)
    socketio.run(app, host='0.0.0.0', port=8080, debug=False, allow_unsafe_werkzeug=True)
