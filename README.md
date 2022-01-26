# Discord Time-Tracking-Bot

## Installation
- `pip install -r requirements.txt`
- Set `DISCORD_TOKEN` to your bot's Discord Token
- Add `db.json` and put `{}` inside of it

## Usage

Run `python bot.py`

Chat-Commands:
- `ot @USER1 @USER2 ... @USERN` - Shows online time of users USER[1-n]
- `ot leaderboard` - Shows the 10 most active users of current Server
- `ot leaderboard [NUM<101]` Shows the NUM most active users of current Server
- `ot delta leaderboard` Shows the 10 most active users with the Time Delta to the next place
- `ot graph` Shows a graph of the 10 most active users

