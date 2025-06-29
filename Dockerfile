FROM python:3.13.3-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

RUN flask db init
RUN flask db migrate
RUN flask db upgrade

CMD ["./run.sh"]