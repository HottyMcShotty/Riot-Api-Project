import discord
from discord.ext import commands

# Intents setup (required for certain events and interactions)
intents = discord.Intents.default()
intents.messages = True

# Bot prefix and initialization
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: When the bot is ready
@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

# Command 1: Ping command
@bot.command()
async def ping(ctx):
    """Replies with Pong! and the bot's latency."""
    latency = round(bot.latency * 1000)  # Convert seconds to milliseconds
    await ctx.send(f"Pong! Latency: {latency}ms")

# Command 2: Say command
@bot.command()
async def say(ctx, *, message: str):
    """Repeats the user's message."""
    await ctx.send(message)

# Command 3: Add command
@bot.command()
async def add(ctx, a: int, b: int):
    """Adds two numbers and returns the result."""
    result = a + b
    await ctx.send(f"The sum of {a} and {b} is {result}.")

# Run the bot (replace 'your_token_here' with your bot's token)
bot.run("your_token_here")