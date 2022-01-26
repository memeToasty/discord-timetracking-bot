FROM python:3-slim
WORKDIR /src
COPY bot.py requirements.txt ./

RUN pip3 install -r requirements.txt
RUN pip3 install matplotlib

ENTRYPOINT [ "python", "bot.py" ]