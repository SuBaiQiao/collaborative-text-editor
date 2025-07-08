import os

from flask import Flask, request, send_file
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 900
socketio = SocketIO(app, ping_timeout=900, ping_interval=300)

# 文件存储目录
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 文本持久化存储
TEXT_FOLDER = 'data'
app.config['TEXT_FOLDER'] = TEXT_FOLDER
TEXT_FILE_NAME = 'content.txt'
app.config['TEXT_FILE_NAME'] = TEXT_FILE_NAME

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


def load_all_files(directory):
    for filename in os.listdir(directory):
        file_list.append(filename)


def load_text(directory, filename):
    file = os.path.join(directory, filename)
    text = ''
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()
        f.close()
    text_history.append(text)


@app.route('/')
def index():
    return send_file('templates/index.html')


@socketio.on('text_update')
def handle_text_update(data):
    # 更新文本并将其添加到历史记录中
    new_text = data['text']
    if new_text != (text_history[-1] if text_history else ""):
        text_history.append(new_text)
        socketio.emit('text_update', {'text': new_text})  # 广播新文本
    with open(os.path.join(app.config['TEXT_FOLDER'], app.config['TEXT_FILE_NAME']), 'w', encoding='utf-8') as f:
        f.write(new_text)
    f.close()


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


@app.route('/delete/<filename>', methods=['GET'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        return 'File deleted successfully', 200
    os.unlink(file_path)
    file_list.remove(filename)
    socketio.emit('file_list_update', {'file_list': file_list})
    return 'File deleted successfully', 200


# 为什么要放外面？因为使用gunicorn启动的时候是不会执行main方法的
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(TEXT_FOLDER):
    os.makedirs(TEXT_FOLDER)
# remove_all_files(UPLOAD_FOLDER)
load_text(TEXT_FOLDER, TEXT_FILE_NAME)
load_all_files(UPLOAD_FOLDER)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=False, allow_unsafe_werkzeug=True)
