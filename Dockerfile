FROM python:3.10

COPY pip.conf /root/.pip/pip.conf
RUN mkdir -p /code
WORKDIR /code
COPY ./static ./static
COPY ./templates ./templates
COPY ./app.py ./app.py

# 安装依赖
RUN pip install Flask Flask-SocketIO gunicorn gevent
EXPOSE 8080

# 使用 gunicorn 启动应用
CMD ["gunicorn", "-k", "gevent", "-w", "1", "--bind", "0.0.0.0:8080", "app:app"]