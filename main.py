import discord
from discord.ext import commands
import requests
import time
import tkinter as tk
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="Riot-Api-Project\.env")
API_KEY=str(os.getenv("API_KEY"))
print(API_KEY)
#name="Autolykus"#"The%20Troglodyte"
#id="NA1"#"1111"
kda =0
playerList=[None]*10
BOT_KEY = os.getenv("BOT_KEY")
statList=[None]*10



async def obtain(ctx, result, userid):
    api_url="https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"+result+"/"+userid+"?api_key="+API_KEY
    if(requests.get(api_url).status_code) != 200:
        await ctx.send("Invalid User Data")
        print(requests.get(api_url))
    else:
        totalkda=0
        playerInfo=[]
        #getting the json file, then parsing the json file, and then grabbing the puuid
        puuid=requests.get(api_url).json()["puuid"]
        active_game=requests.get("https://na1.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/"+puuid+"?api_key="+API_KEY)
    
        if active_game.status_code == 200:
            await ctx.send("Current Game Data")
            for x in range(10):
                playerList[x]=active_game.json()['participants'][x]['puuid']
            

        else:
            print(active_game)
            await ctx.send("Past Game Data")
            matches_url="https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"+puuid+"/ids?start=0&count=5&api_key="+API_KEY
            lastMatch=requests.get(matches_url).json()[0]
            lastMatchurl="https://americas.api.riotgames.com/lol/match/v5/matches/"+lastMatch+"?api_key="+API_KEY

            #putting all 10 players from current/lastmatch into a list
            for x in range(10):
                playerList[x]=requests.get(lastMatchurl).json()['metadata']["participants"][x]
        

    #obtaining player stats
        for x in range(10):
            winsum=0
            ####Iteating through our player list and getting match ids for their last 10 matches
            matches_url="https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"+playerList[x]+"/ids?start=0&count=5&api_key="+API_KEY
            for y in range(3):
                try:
                    matches=requests.get(matches_url).json()[y]
                    ####
                    ####Making a data call for the first player in game and the match that is equal to index x
                    temp_match="https://americas.api.riotgames.com/lol/match/v5/matches/"+matches+"?api_key="+API_KEY
                    match_data_call=requests.get(temp_match).json()
                    ####Grabbing Data From the Match
                    info=match_data_call['metadata']["participants"].index(playerList[x])
                    kda =match_data_call["info"]["participants"][info]["challenges"]["kda"]
                    win =match_data_call["info"]["participants"][info]["win"]
                    #win =match_data_call["info"]["participants"][info]["win"]
                    vs =match_data_call["info"]["participants"][info]["visionScore"]
                    totalkda=totalkda+kda
                    winsum+=int(win)
                    
                    
                    
                except Exception as e:
                    print(f"An error occurred: {e}")
            winsum/=3
            print(str((1+x)*10)+"% Done!")
            temp_name=match_data_call["info"]["participants"][info]["summonerName"]
            playerInfo.append({"Name":temp_name,"KDA":round((totalkda/3),2),"Win":str(winsum*100)})
            #await ctx.send(f"Name: {temp_name}\tKDA: {round((totalkda/3),2)}\tWin Rate: {str(round((winsum * 100),2))}%")
            statList[x]=({"Name":temp_name,"KDA":round((totalkda/3),2),"Win":str(round((winsum * 100),2))})
            totalkda=0
            win=0
            
            
            ####




def botty():
    intents = discord.Intents.default()
    intents.message_content = True

    # Bot prefix and initialization
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"Bot is online as {bot.user}")

    @bot.command()
    async def ping(ctx, *, message):
        embed=discord.Embed(
            title="Player Stats",
            description="Here are the stats for all the Players",
            color=0x0099ff
        )
        count=20
        nameid = message.split("#",1)
        username=nameid[0]
        userid=nameid[1]
        result = ""
        for char in username:
            if char == " ":
                result += f"%{count}"  
                count += 1            
            else:
                result += char  
        print(result)
        print(userid)
            
        await ctx.send("Gathering Data, this may take a moment")
        await obtain(ctx, result,userid)
        for x in range(10):
            embed.add_field(name=statList[x]["Name"],value=f"KDA: {statList[x]['KDA']:<20} Win Rate: {statList[x]['Win']:<20}% ",inline=False)
        await ctx.send(embed=embed)

    bot.run(BOT_KEY)
botty()