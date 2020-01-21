# massassins_bot2.py
import os
from dotenv import load_dotenv
import sqlite3

from discord.ext import commands
from discord.utils import get

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

@bot.command(name='reset', help="ADMINS ONLY: Resets ALL database tables and entries <ONLY USE ONCE TO RESET GAME>")
async def reset(ctx):
    sql.drop_tables(cur)
    sql.create_tables(cur)

@bot.command(name='populate', help="ADMINS ONLY: Populates the teams with members <ONLY USE ONCE TO RESET GAME>")
async def game_populate(ctx):
    await ctx.send("Processing teams and items...")
    sql.populate_teams_table(cur, settings.team_list)
    sql.populate_items_table(cur, settings.item_dict)
    await ctx.send("Finished processing teams and items, now processing players")
    for player_name,player_team_name in settings.player_team_dict:
        return_code = sql.populate_players_table(cur, player_name, player_team_name)
        if return_code == -1:
            await ctx.send('There has been an error processing team_name, double-check hard-coded team names in player-team-dict')
    await ctx.send("All players has been processed, waiting for players to join...")

@bot.command(name="add_player", help="ADMINS ONLY: Adds a player into the game <DOES NOT CHANGE HARD-CODED PLAYER_TEAM_MAPS>")
async def add_player(ctx, player_name, team_name):
    return_code = sql.populate_players_table(cur, player_name, team_name)
    if return_code == -1:
        await ctx.send("There has been an error, please check team_name is valid")
    await ctx.send("Player {} has been added into the game, waiting for them to join".format(player_name))

@bot.command(name="give_gold", help="ADMINS ONLY: Gives gold to a specific player")
async def give_gold(ctx, player_name, gold_amount):
    try:
        sql.update_player_gold(cur, player_name, gold_amount)
        await ctx.send("Gold has been given to the player {}".format(player_name))
    except:
        await ctx.send("Please try again, command is !give_gold <player_name> <gold_amount>")
    
@bot.command(name="give_team_experience", help="ADMIN ONLY: Gives experience to a specific team : !give_team_experience <team_name> <experience_amount>")
async def give_team_experience(ctx, team_name, experience_amount):
    try:
        sql.update_team_experience(team_name, experience_amount)
        await ctx.send("Experience has been given to team {}".format(team_name))
    except:
        await ctx.send("Giving experience has caused an error")

@bot.command(name="join", help="As a member, if you are signed up for Masassins and admins have coded you in, join processes you as a valid player in the game")
async def join(ctx):
    player_display_name = ctx.message.author.name
    await ctx.send("Hello {} please wait while we process your join request".format(player_display_name))
    if player_display_name in settings.player_team_dict:
        member = ctx.message.author
        masassins_role = get(member.server.roles, name="Pokemon Trainer")
        team_role = get(member.server.roles, name=settings.player_team_dict[player_display_name])
        await bot.add_roles(member, masassins_role)
        await bot.add_roles(member, team_role)
        await ctx.send("Hello {}, we found your name in our database so you will now be given your team and corresponding roles")
    else:
        await ctx.send("Sorry your name was not found, please contact the admins")

@bot.command(name='use', help='Use an item!')
async def use_an_item(ctx, item_name):
   if item_name == "Potion":
       player_name = ctx.message.author.name 
       sql.update_player_hp(cur, player_name, 50)

@bot.command(name="attack", help="Attack a player : !attack player_name")
async def attack(ctx, player_name): #Maybe consider instead of inputting names, use mention
    attacking_player = ctx.message.author.name

    await ctx.send("Hello {} you are attacking {}".format(attacking_player, defending_player))

    #Create a message to send to defending player, and wait for response for X amount of time
    #def check(m):
    #    return m.content == 'confirm'

    #msg = await bot.wait_for('message', timeout=60.0, check=check)
    
bot.run(token)