# bot.py
import os
import json

import discord
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
INTERVAL = 60 # Seconds
PREFIX = "ot"

intents = discord.Intents.default()
intents.members = True

def convert(time):
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    return f"{day} d {hour} h {minutes} m {seconds} s"

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db_name = "db.json"
        self.startup = True
        # start the task to run in the background
        self.my_background_task.start()

    def read_db(self):
        with open(self.db_name, 'r') as openfile:
            # Reading from json file
            return json.load(openfile)

    def write_db(self, dataset):
        with open(self.db_name, "w") as outfile:
            json.dump(dataset, outfile, indent=4)
        
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    @tasks.loop(seconds=INTERVAL)
    async def my_background_task(self):
        if self.startup:
            self.startup = False
            return
        
        dataset = self.read_db()
        for guild in self.guilds:

            if str(guild.id) not in dataset:
                dataset[str(guild.id)] = {}
            
            for channel in guild.voice_channels:

                if "AFK" in channel.name:
                    continue

                for member in channel.members:
                    if member.voice.afk or member.voice.deaf or member.voice.self_deaf:
                        continue
                    if str(member.id) not in dataset[str(guild.id)]:
                        dataset[str(guild.id)][str(member.id)] = INTERVAL
                    else:
                        dataset[str(guild.id)][str(member.id)] += INTERVAL

        self.write_db(dataset)
                
        

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready() # wait until the bot logs in
    
    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        
        if message.content.startswith(PREFIX):
            if "leaderboard" in message.content:
                dataset = self.read_db()
                marklist = sorted(dataset[str(message.guild.id)].items(), key=lambda x:x[1], reverse=True)
                sortdict = dict(marklist)
                sortlist = [(k, v) for k, v in sortdict.items()]
                reply_str = f"Top 10 most active {message.guild.name}-users:\n"
                
                for x in range(0,  9):
                    try:
                        reply_str += f"{x + 1}. <@{str(sortlist[x][0])}> | {convert(sortlist[x][1])}\n"
                    except:
                        reply_str += f"{x + 1}. ----\n"

                await message.reply(reply_str, mention_author=True)
            
            elif len(message.mentions) != 0:
                dataset = self.read_db()
                reply_str = ""
                for user in message.mentions:
                    try:
                        time_string = convert(dataset[str(message.guild.id)][str(user.id)])
                        reply_str += f"<@{user.id}> has an online-time of: {time_string}\n"
                    except:
                        reply_str += f"<@{user.id}> has no online-time\n"
                await message.reply(reply_str, mention_author=True)
            else:
                await message.reply('There is no mention for this user', mention_author=True)

client = MyClient(intents=intents)
client.run(TOKEN)
