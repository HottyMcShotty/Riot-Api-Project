import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv(dotenv_path="C:/Users/samue/OneDrive/Desktop/LeagueCompanion/Riot-Api-Project/.env")
BOT_KEY = os.getenv("BOT_KEY")
print(f"Loaded BOT_KEY: {BOT_KEY}")  # Debugging line

if BOT_KEY is None:
    raise ValueError("BOT_KEY is not set. Check your .env file.")

# Intents setup
intents = discord.Intents.default()
intents.messages = True

# Bot prefix and initialization
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! Latency: {latency}ms")

@bot.command()
async def say(ctx, *, message: str):
    await ctx.send(message)

@bot.command()
async def add(ctx, a: int, b: int):
    result = a + b
    await ctx.send(f"The sum of {a} and {b} is {result}.")

bot.run(BOT_KEY)
