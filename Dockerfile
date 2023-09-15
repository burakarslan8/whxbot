FROM python:3.11-alpine3.17

WORKDIR /bot

COPY . /bot

RUN pip install -r requirements.txt

EXPOSE 80

ENV NAME World

CMD ["python","bot.py"]