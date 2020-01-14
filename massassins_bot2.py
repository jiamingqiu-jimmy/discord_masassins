# massassins_bot2.py
import os
from dotenv import load_dotenv
import sqlite3

from discord.ext import commands

#Local Files import
import settings
import sql_functions as sql

#Sqlite3 DB connection
conn = sqlite3.connect('masassins.db')
#Creating sqlite3 db cursor
cur = conn.cursor()

#Load Environment
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='reset', help="ADMINS ONLY: Resets ALL database tables and entries")
async def reset(ctx):
    sql.drop_tables(cur)
    sql.create_tables(cur)

@bot.command(name='populate', help="ADMIN: Populates the teams with members")
async def game_populate(ctx):
    sql.populate_teams_table(cur, settings.team_list)
    sql.populate_items_table(cur, settings.item_dict)
    sql.populate_players_table(cur, settings.player_team_dict)

@bot.command(name="give_gold", help "ADMIN: Gives gold to a specific player")
async def give_gold(ctx):


@bot.command(name='go', help='Starts up the game')
async def game_start_up(ctx): #Ctx is context (Holds data such as channel and guild that user called the command from)
    #Grabs a list of all the members in the assigned roles

    #Sends out introductory message and first "mission" 

    #Sends out pings to all users and immediately 
    return

@bot.command(name='use', help='Use an item!')
async def use_an_item(ctx):
    return
bot.run(token)