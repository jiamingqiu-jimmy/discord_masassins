# massassins_bot2.py
import os
from dotenv import load_dotenv
import discord
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

@bot.event
async def on_ready():
    print('{} has connected to Discord!'.format(bot.user.name))

@bot.command(name='reset', help="ADMINS ONLY: Resets ALL database tables, entries and roles <ONLY USE ONCE TO RESET GAME>")
@commands.has_role(settings.admin_role)
async def reset(ctx):
    await ctx.send("Dropping tables...")
    sql.drop_tables(cur)
    await ctx.send("Recreating tables...")
    sql.create_tables(cur)
    await ctx.send("Database tables have been dropped and recreated")

    await ctx.send("Deleting all masassin roles...")

    guild = ctx.guild
    masassins_role = get(guild.roles, name=settings.masassins_role)

    if masassins_role is not None:
        await masassins_role.delete()
        await ctx.send("The Masassins role is deleted")

@reset.error
async def reset_error(ctx, error):
    await ctx.send(error)

@bot.command(name='populate', help="ADMINS ONLY: Populates the teams with members <ONLY USE ONCE TO RESET GAME>")
async def game_populate(ctx):
    await ctx.send("Processing teams and items...")
    sql.populate_teams_table(cur, settings.team_list)
    sql.populate_items_table(cur, settings.item_dict)
    await ctx.send("Finished processing teams and items, now processing players")
    for player_name,player_team_name in settings.player_team_dict.items():
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
async def give_gold(ctx, team_name, gold_amount):
    try:
        sql.update_team_gold(cur, team_name, gold_amount)
        await ctx.send("Gold has been given to the player {}".format(player_name))
    except:
        await ctx.send("Please try again, command is !give_gold <team_name> <gold_amount>")
    
@bot.command(name="give_team_experience", help="ADMIN ONLY: Gives experience to a specific team : !give_team_experience <team_name> <experience_amount>")
async def give_team_experience(ctx, team_name, experience_amount):
    try:
        sql.update_team_experience(cur, team_name, experience_amount)
        await ctx.send("Experience has been given to team {}".format(team_name))
    except:
        await ctx.send("Giving experience has caused an error")

@bot.command(name="join", help="As a member, if you are signed up for Masassins and admins have coded you in, join processes you as a valid player in the game")
async def join(ctx):
    player_display_name = ctx.message.author.name
    guild = ctx.message.author.guild
    await ctx.send("Hello {} please wait while we process your join request at {}".format(player_display_name, guild.name))
    if player_display_name in settings.player_team_dict:
        team_name = settings.player_team_dict[player_display_name]

        member = ctx.message.author
        guild = member.guild

        masassins_role = get(guild.roles, name=settings.masassins_role)
        team_role = get(guild.roles, name=team_name)

        if masassins_role is None:
            await ctx.send("The Masassins role is not found, creating new role...")
            masassins_role = await guild.create_role(name=settings.masassins_role)
            await ctx.send("The Masassins role is created")
        if team_role is None:
            await ctx.send("The Team Role is not found, creating new team role {} ...".format(team_name))
            team_role = await guild.create_role(name=team_name)
            await ctx.send("The Team Role {} is created".format(team_name))

        await member.add_roles(masassins_role)
        await member.add_roles(team_role)
        await ctx.send("Hello {}, we found your name in our database so you will now be given your team and corresponding roles".format(player_display_name))
        await ctx.send("Hello {}, your team is {}".format(player_display_name, team_role))

    else:
        await ctx.send("Sorry your name was not found, please contact the admins")

@bot.command(name='use', help='Use an item!')
async def use_an_item(ctx, item_name):
   if item_name == "Potion":
       player_name = ctx.message.author.name 
       sql.update_player_hp(cur, player_name, 50)
       await ctx.send("You have used a potion!")

@bot.command(name="attack", help="Attack a player : !attack player_name")
async def attack(ctx, player_name): #Maybe consider instead of inputting names, use mention
    attacking_player = ctx.message.author.name

    await ctx.send("Hello {} you are attacking {}".format(attacking_player, defending_player))

    #Create a message to send to defending player, and wait for response for X amount of time
    #def check(m):
    #    return m.content == 'confirm'

    #msg = await bot.wait_for('message', timeout=60.0, check=check)
    
bot.run(token)