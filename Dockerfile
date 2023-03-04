FROM python:3.8.13

COPY . /chathawk

WORKDIR /chathawk

RUN pip install -r requirements.txt

CMD ["python", "./bot/bot.py"]
