# bot.py
import os
import json

import discord
from discord.ext import tasks
from dotenv import load_dotenv
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["figure.autolayout"] = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
INTERVAL = 60 # Seconds
PREFIX = "ot"

intents = discord.Intents.default()
intents.members = True

def convert(time):
    return_str = ""
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    if day != 0:
        return_str += f"{day} d "
    if hour != 0:
        return_str += f"{hour} h "
    if minutes != 0:
        return_str += f"{minutes} m"
    if seconds != 0:
        return_str += f" {seconds} s"
    return return_str

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db_name = "data/db.json"
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
        await self.change_presence(activity=discord.Game(name="👀"))

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
                
    def getRankings(self, message):
        dataset = self.read_db()
        marklist = sorted(dataset[str(message.guild.id)].items(), key=lambda x:x[1], reverse=True)
        sortdict = dict(marklist)
        return [(k, v) for k, v in sortdict.items()]

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready() # wait until the bot logs in
    
    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        
        if message.content.startswith(PREFIX):
            if "leaderboard" in message.content:
                top_count = 10
                deltaFlag = False
                if message.content.split(' ')[-1] != "leaderboard":
                    top_count = int(message.content.split(' ')[-1])
                
                if "delta" in message.content:
                    deltaFlag = True
                if top_count > 100:
                    await message.reply("The requested number is too large", mention_author=True)
                    return
                sortlist = self.getRankings(message)
                reply_str = f"Top {top_count} most active {message.guild.name}-users:\n"
                

                if len(sortlist) < top_count:
                    top_count = len(sortlist)
                for x in range(0,  top_count):
                    matchingMember = discord.utils.find(lambda m: m.id == int(sortlist[x][0]), message.guild.members)
                    if matchingMember is not None:
                        reply_str += f"{x + 1}. {matchingMember.name} | {convert(sortlist[x][1])} "
                    else:
                        reply_str += f"{x + 1}. unknown User | {convert(sortlist[x][1])} "
                    if x > 0 and deltaFlag:
                        reply_str += f"| Δ{convert(sortlist[x-1][1] - sortlist[x][1])}"
                    reply_str += "\n"
                await message.reply(reply_str, mention_author=True)
            
            elif len(message.mentions) != 0:
                dataset = self.read_db()
                reply_str = ""
                for user in message.mentions:
                    try:
                        time_string = convert(dataset[str(message.guild.id)][str(user.id)])
                        matchingMember = discord.utils.find(lambda m: m.id == int(sortlist[x][0]), message.guild.members)
                        if matchingMember is not None:
                            reply_str += f"{matchingMember.name} has an online-time of: {time_string}\n"
                        else:
                            reply_str += f"unknown User has an online-time of: {time_string}\n"
                    except:
                        reply_str += f"This user has no online-time\n"
                await message.reply(reply_str, mention_author=True)
            elif "graph" in message.content:
                sortlist = self.getRankings(message)

                height = []
                bars = []

                for x in range(len(sortlist)):
                    height.append(sortlist[x][1] / 3600)
                    matchingMember = discord.utils.find(lambda m: m.id == int(sortlist[x][0]), message.guild.members)
                    if matchingMember is not None:
                        bars.append(matchingMember.name)
                    else:
                        bars.append("Unknown")
                yPos = np.arange(len(bars))

                fig = plt.figure()
                plt.barh(yPos, height)
                plt.yticks(yPos, bars)
                plt.xlabel("Onlinetime in h")
                fig.subplots_adjust(left=0.5)
                plt.savefig("graph.png")
                with open("graph.png", "rb") as graphFile:
                    graph = discord.File(graphFile, filename="graph.png")
                await message.reply(file=graph)


            else:
                await message.reply('There is no mention for this user', mention_author=True)

client = MyClient(intents=intents)
client.run(TOKEN)
