import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import main
from main import obtain

# Load the .env file
load_dotenv(dotenv_path="C:/Users/samue/OneDrive/Desktop/LeagueCompanion/Riot-Api-Project/.env")
BOT_KEY = os.getenv("BOT_KEY")
print(f"Loaded BOT_KEY: {BOT_KEY}")  # Debugging line``

intents = discord.Intents.default()
intents.message_content = True

# Bot prefix and initialization
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send(obtain())

bot.run(BOT_KEY)
