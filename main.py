import discord
from discord.ext import commands
import requests
import time
import json
import tkinter as tk
import os
from dotenv import load_dotenv
import asyncio
from functools import lru_cache

with open("imgs.json", "r") as f:
    champIcons=json.load(f)

# Load .env variables
load_dotenv(dotenv_path=".env")
API_KEY = str(os.getenv("API_KEY"))
BOT_KEY = str(os.getenv("BOT_KEY"))

playerList = [None] * 10
statList = [None] * 10

# Rate limiter
semaphore = asyncio.Semaphore(5)  # Limit to 5 concurrent requests

@lru_cache(maxsize=128)
def get_api_data(url):
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

async def obtain(ctx, result, userid):
    api_url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{result}/{userid}?api_key={API_KEY}"
    
    async with semaphore:
        data = get_api_data(api_url)
        if not data:
            await ctx.send("Invalid User Data")
            return
        
        puuid = data["puuid"]
        active_game_url = f"https://na1.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}?api_key={API_KEY}"
        active_game = get_api_data(active_game_url)
        
        if active_game:
            await ctx.send("Current Game Data")
            for x in range(10):
                playerList[x] = active_game['participants'][x]['puuid']
        else:
            await ctx.send("Past Game Data")
            matches_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=10&api_key={API_KEY}"
            lastMatch = get_api_data(matches_url)[0]
            lastMatchurl = f"https://americas.api.riotgames.com/lol/match/v5/matches/{lastMatch}?api_key={API_KEY}"

            for x in range(10):
                playerList[x] = get_api_data(lastMatchurl)['metadata']["participants"][x]

        totalkda = 0
        playerInfo = []
        for x in range(10):
            winsum = 0
            matches_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{playerList[x]}/ids?start=0&count=10&api_key={API_KEY}"
            

            for y in range(4, -1, -1):
                try:
                    matches = get_api_data(matches_url)[y]
                    temp_match = f"https://americas.api.riotgames.com/lol/match/v5/matches/{matches}?api_key={API_KEY}"
                    match_data_call = get_api_data(temp_match)
                    info = match_data_call['metadata']["participants"].index(playerList[x])
                    kda = match_data_call["info"]["participants"][info]["challenges"]["kda"]
                    win = match_data_call["info"]["participants"][info]["win"]
                    champ=match_data_call["info"]["participants"][info]["championName"]
                    
                    totalkda += kda
                    winsum += int(win)
                except Exception as e:
                    print(f"An error occurred: {e}")
            winsum /= 10
            print(str((1 + x) * 10) + "% Done!")
            temp_name = match_data_call["info"]["participants"][info]["summonerName"]
            playerInfo.append({"Name": temp_name, "KDA": round((totalkda / 10), 2), "Win": str(winsum * 100)})
            statList[x] = {"Name": temp_name, "KDA": round((totalkda / 10), 2), "Champ":champ, "Win": str(round((winsum * 100), 2))}
            totalkda = 0
            win = 0

def botty():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"Bot is online as {bot.user}")

    @bot.command()
    async def ping(ctx, *, message):
        embed = discord.Embed(
            title="Player Stats",
            description="Here are the stats for all the Players",
            color=0x99ff
        )
        count = 20
        nameid = message.split("#", 1)
        username = nameid[0]
        userid = nameid[1]
        result = ""
        for char in username:
            if char == " ":
                result += f"%{count}"
                count += 1
            else:
                result += char

        await ctx.send("Gathering Data, this may take a moment")
        await obtain(ctx, result, userid)

        column1=""
        column2=""
        for x in range(10):
            player_stats = f"{champIcons[statList[x]['Champ']]} {statList[x]['Name']}\nKDA: {statList[x]['KDA']:<20}\nWin Rate: {statList[x]['Win']:<20}%\n\n"
            if x < 5:
                column1 += player_stats
            else:
                column2 += player_stats
        embed.add_field(name="Column 1", value=column1, inline=True)
        embed.add_field(name="Column 2", value=column2, inline=True)

        await ctx.send(embed=embed)
    bot.run(BOT_KEY)

botty()