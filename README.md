# collaborative-text-editor
多端文件复制项目-Python

### 下载项目
```bash
git clone https://github.com/SuBaiQiao/collaborative-text-editor.git
```

### 运行项目
1. 确保您已安装 Flask 和 Flask-SocketIO：
   ```bash
   pip install Flask Flask-SocketIO
   ```

2. 在命令行中运行 Flask 应用程序：
   ```bash
   python app.py
   ```

3. 打开浏览器并访问 `http://127.0.0.1:5000`，您将能够看到实时文本编辑器的界面。

通过以上步骤，您将创建一个多用户实时协作的文本编辑器，所有用户可以在同一文本框中并行编辑，并且所有更改都会即时反映在其他用户的界面上。