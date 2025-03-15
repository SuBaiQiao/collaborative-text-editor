# collaborative-text-editor
多端文本复制项目-Python

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

## 如果你想使用docker镜像进行部署，那么你需要自己打包镜像
```bash
docker build -t collaborative-text-editor:1.0 .
```
镜像打包完成后使用`docker run`命令进行运行

注意：18080是我本地的端口号，可以根据自己的端口号进行修改
```bash
docker run -id --name collaborative-text-editor -p 18080:8080 collaborative-text-editor:1.0
```

运行完成后网页访问`http://localhost:18080/` 即可