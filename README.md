# Discord Time-Tracking-Bot

## Installation
### Without Docker
- `pip install -r requirements.txt`
- Set `DISCORD_TOKEN` to your bot's Discord Token

### With Docker
- get the latest Image via `docker pull ghcr.io/memetoasty/discord-timetracking-bot:latest`
- start the container using `docker run --rm -it -e DISPLAY --name activity_bot -v ./data:/src/data -e DISCORD_TOKEN={BOT TOKEN}`

## Usage

Run `python bot.py`

Chat-Commands:
- `ot leaderboard` - Shows the 10 most active users of current Server
- `ot leaderboard [NUM<101]` Shows the NUM most active users of current Server
- `ot delta leaderboard` Shows the 10 most active users with the Time Delta to the next place
- `ot delta1 leaderboard` Shows the 10 most active users with the Time Delta to the first place
- `ot graph` Shows a graph of the most active users