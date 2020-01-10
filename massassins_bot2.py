# massassins_bot2.py
import os
from dotenv import load_dotenv
import sqlite3

from discord.ext import commands

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

@bot.command(name='populate', help="ADMIN: Populates the teams with members")
async def game_populate(ctx):
    
    valid_team_check = """
    SELECT * FROM teams WHERE name=?
    """

    for name, team_type in player_team_dict.items():
        try:
            cur.execute(valid_team_check, team_type)
            rows = cur.fetchall()
            if len(rows) == 0:
                await self.send("One of the teams listed was not found in the database, please double check input values")
                return
        except sqlite3.Error:
            await self.send("Failed to populate members, error occured")
            return

    # After confirming that all the teams were there
    find_team_id = """
    SELECT team_id FROM teams where name=?
    """

    populate_players_table = """
    INSERT INTO players (name, health, gold, team_id) VALUES (?,?,?,?)
    """

    for name, team_type in player_team_dict.items():
        cur.execute(find_team_id, team_type)
        r = cur.fetchone()
        new_player = (name, new_player_starting_health, new_player_starting_gold, r['team_id'])
        cur.execute(populate_players_table,new_player)

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