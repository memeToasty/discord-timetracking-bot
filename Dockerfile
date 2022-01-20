FROM python:alpine
WORKDIR /src
COPY bot.py requirements.txt ./

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "bot.py" ]