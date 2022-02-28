FROM python:3-slim
WORKDIR /src
LABEL org.opencontainers.image.source = "https://github.com/memeToasty/discord-timetracking-bot"
COPY bot.py requirements.txt ./

RUN pip3 install -r requirements.txt
RUN pip3 install matplotlib

ENTRYPOINT [ "python", "bot.py" ]