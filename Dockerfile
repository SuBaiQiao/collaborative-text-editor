FROM python:3.13.0

COPY pip.conf /root/.pip/pip.conf
RUN mkdir -p /code
WORKDIR /code
COPY ./ ./

RUN pip install Flask
RUN pip install Flask-SocketIO
EXPOSE 8080

CMD ["python", "app.py"]