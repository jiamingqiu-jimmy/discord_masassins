import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
bot = commands.Bot(command_prefix='>')

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say("pong")

bot.run(token)