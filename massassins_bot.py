# massassins_bot.py
import os
from dotenv import load_dotenv
import discord
import sqlite3

from discord.ext import commands
from discord.utils import get

#Local Files import
import settings
import sql_functions as sql
import battle_functions as battle

#Sqlite3 DB connection
conn = sqlite3.connect('masassins.db')

#Load Environment
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
client = discord.Client()

@bot.event
async def on_ready():
    print('{} has connected to Discord!'.format(bot.user.name))

@bot.command(name='reset', help="ADMINS ONLY: Resets ALL database tables, entries and roles <ONLY USE ONCE TO RESET GAME>")
@commands.is_owner()
async def reset(ctx):
    #Creating sqlite3 db cursor
    cur = conn.cursor()

    await ctx.send("Dropping tables...")
    sql.drop_tables(cur)
    await ctx.send("Recreating tables...")
    sql.create_tables(cur)
    await ctx.send("Database tables have been dropped and recreated")

    await ctx.send("Deleting all masassin roles...")

    guild = ctx.guild

    for role in settings.base_masassins_roles:
        masassins_role = get(guild.roles, name=role)

        if masassins_role is not None:
            await masassins_role.delete()
            await ctx.send("The {} role is deleted".format(role))

    await ctx.send("Deleting team roles...")
    
    for team_name in settings.team_list:
        team_role = get(guild.roles, name=team_name)
        if team_role is not None:
            await team_role.delete()
            await ctx.send("The team role : '{}' is deleted".format(team_name))

    await ctx.send("All resetting procedures are done!")

@reset.error
async def reset_error(ctx, error):
    await ctx.send(error)

@bot.command(name='populate', help="ADMINS ONLY: Populates the teams with members <ONLY USE ONCE TO RESET GAME>")
@commands.is_owner()
async def game_populate(ctx):
    #Creating sqlite3 db cursor
    cur = conn.cursor()

    #Populating pre-set items and teams
    await ctx.send("Processing teams and items...")
    sql.populate_teams_table(cur, settings.team_list)
    sql.populate_items_table(cur, settings.item_dict)

    guild = ctx.guild
    masassins_dead_role = get(guild.roles, name=settings.masassins_dead_role)
    #Creating all the necessary roles
    if masassins_dead_role is None:
        await ctx.send("Creating masassins-fainted role...")
        masassins_dead_role = await guild.create_role(name=settings.masassins_dead_role)
        await ctx.send("The Masassins-fainted role is created")

    masassins_alive_role = get(guild.roles, name=settings.masassins_alive_role)

    if masassins_alive_role is None:
        await ctx.send("Creating masassins-alive role...")
        masassins_alive_role = await guild.create_role(name=settings.masassins_alive_role)
        await ctx.send("The Massassins-alive role is created")

    for team_name in settings.team_list:
        team_role = get(guild.roles, name=team_name)
        if team_role is None:
            await ctx.send("Creating new team role {} ...".format(team_name))
            team_role = await guild.create_role(name=team_name)
            await ctx.send("The Team Role {} is created".format(team_name))

    #Processing the players
    await ctx.send("Finished processing teams and items, now processing players")
    for player_name,player_team_name in settings.player_team_dict.items():
        return_code = sql.populate_players_table(cur, player_name, player_team_name)
        if return_code == -1:
            await ctx.send('There has been an error processing team_name, double-check hard-coded team names in player-team-dict')
        else:
            await ctx.send("{} has been processed...".format(player_name))
    await ctx.send("All players has been processed, waiting for players to join...")

@bot.command(name="add_player", help="ADMINS ONLY: Adds a player into the game <DOES NOT CHANGE HARD-CODED PLAYER_TEAM_MAPS>")
@commands.has_role(settings.admin_role)
async def add_player(ctx, player_name, team_name):
    return_code = sql.populate_players_table(cur, player_name, team_name)
    if return_code == -1:
        await ctx.send("There has been an error, please check team_name is valid")
    await ctx.send("Player {} has been added into the game, waiting for them to join".format(player_name))

@bot.command(name="give_gold", help="ADMINS ONLY: Gives gold to a specific player")
@commands.has_role(settings.admin_role)
async def give_gold(ctx, team_name, gold_amount):

    cur = conn.cursor()
    sql.update_team_gold(cur, team_name, gold_amount)
    await ctx.send("{} Gold has been given to the team {}".format(gold_amount, team_name))

@bot.command(name="give_team_experience", help="ADMIN ONLY: Gives experience to a specific team : !give_team_experience <team_name> <experience_amount>")
@commands.has_role(settings.admin_role)
async def give_team_experience(ctx, team_name, experience_amount):
    cur = conn.cursor()
    sql.update_team_experience(cur, team_name, experience_amount)
    await ctx.send("{} EXP has been given to team {}".format(experience_amount, team_name))

@bot.command(name="create_channels", help="ADMINS ONLY: Create all the team channels and text channels for masassins")
@commands.has_role(settings.admin_role)
async def create_channels(ctx):
    await ctx.send("Creating all necessary channels...")
    guild = ctx.guild
    masassins_channel = await guild.create_category_channel(settings.masassins_category_channel_name)
    await ctx.send("Created Category Channel")
    all_team_channel_overwrite = {
        guild.default_role: discord.PermissionOverwrite(read_messages=True)
    }
    await masassins_channel.create_text_channel(name=settings.masassins_all_team_channel_name, overwrites=all_team_channel_overwrite, position=0)
    await ctx.send("Created All-Team Discussion Channel")

    for team_name in settings.team_list:
        team_role = get(guild.roles, name=team_name)
        admin_role = get(guild.roles, name=settings.admin_role)
        team_channel_overwrite = {
            admin_role: discord.PermissionOverwrite(read_messages=True),
            team_role: discord.PermissionOverwrite(read_messages=True),
            guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }
        await masassins_channel.create_text_channel(name=team_name, overwrites=team_channel_overwrite)
        await ctx.send("Created {} Discussion Channel".format(team_name))
    
@bot.command(name="delete_channels", help="ADMINS ONLY: Delete all the team channels and text channels for masassins")
@commands.has_role(settings.admin_role)
async def delete_channels(ctx):
    guild = ctx.guild

    channels_list = guild.channels
    for channel in channels_list:
        print(channel.name)
        for base_channel_name in settings.base_channels_namelist:
            if base_channel_name.lower() == channel.name.lower():
                await ctx.send("Deleting {}...".format(base_channel_name))
                await channel.delete()
                await ctx.send("Deleted {}".format(base_channel_name))
        for team_name in settings.team_list:
            if channel.name.lower() == team_name.lower():
                await ctx.send("Deleting {} channel...".format(team_name))
                await channel.delete()
                await ctx.send("Deleted {} channel".format(team_name))

    await ctx.send("Complete!")

@bot.command(name="join", help="As a member, if you are signed up for Masassins and admins have coded you in, join processes you as a valid player in the game")
async def join(ctx):
    cur = conn.cursor()
    player_display_name = ctx.author.name
    guild = ctx.guild
    await ctx.send("Hello {} please wait while we process your join request at {}".format(player_display_name, guild.name))
    if sql.valid_player_check(cur, player_display_name) == 0:
        team_name = sql.find_team_name_from_player(cur, player_display_name)

        member = ctx.message.author
        guild = member.guild

        masassins_role = get(guild.roles, name=settings.masassins_alive_role)
        team_role = get(guild.roles, name=team_name)
        await member.add_roles(masassins_alive_role)
        await member.add_roles(team_role)
        await ctx.send("Hello {}, we found your name in our database so you will now be given your team and corresponding roles".format(player_display_name))
        await ctx.send("Hello {}, your team is {}".format(player_display_name, team_role))
    else:
        await ctx.send("Sorry your name was not found, please contact the admins")

@bot.command(name='use', help='Use an item!')
@commands.has_any_role(settings.admin_role, settings.masassins_alive_role)
async def use_an_item(ctx, item_name, player_name):
    cur = conn.cursor()
    init_player = ctx.author

    #Init_player_team_name
    init_player_team_name = sql.find_team_name_from_player(cur, init_player.name)

    #Get the player's current team
    team_name = sql.find_team_name_from_player(cur, player_name)

    #Check to see if the team listed is the player's team
    if (init_player_team_name != team_name):
        ctx.send("Item must be used on a player in the same team. Function is !use <item_name> <player_name>")
        return

    #Check to see if it is a valid item
    if (sql.valid_item_check(cur, item_name) != 0):
        ctx.send("Please check that the item name is correct")
        return

    #Check to see if the current team owns the item
    if sql.find_team_item(cur, init_player_team_name, item_name) == 0:
        ctx.send("Your team does not currently own this item")
        return

    #Calculate whether or not 
    if item_name == settings.item_name_potion:
        sql.update_player_hp(cur, player_name, 50)
        await ctx.send("You have used a potion! you have gained {} health".format("50"))


@use_an_item.error
async def use_an_item_error(ctx,error):
    ctx.send(error)

@bot.command(name="attack", help="Attack a player : !attack player_name")
async def attack(ctx, player_name): #Maybe consider instead of inputting names, use mention
    cur = conn.cursor()
    guild = ctx.guild
    attacking_player = ctx.author
    defending_player = get(ctx.guild.members, name=player_name)

    #Check for a valid player in the database
    if sql.valid_player_check(cur, defending_player.name) != 0 or defending_player is None:
        await ctx.send("Please check that you have the right player, the command is !attack <player_name>")
        return 

    #Send message into the player's team channel asking for confirmation use @mention
    defending_player_team = sql.find_team_name_from_player(cur, defending_player.name)
    attacking_player_team = sql.find_team_name_from_player(cur, attacking_player.name)

    defending_player_channel = get(guild.text_channels, name=defending_player_team.lower())

    if defending_player_team.lower() == attacking_player_team.lower():
        await ctx.send("You cannot attack players from the same team!")
        return

    #Wait for confirmation, 60 second deadline or auto-cancel
    message = """
        Hello team {}, {} has just initiated a hit on {}. 
        {} you have 60 seconds to confirm otherwise hit will be cancelled. Type in CONFIRM to confirm the hit """
    message.format(defending_player_team, attacking_player.name, defending_player.name, defending_player.mention)
    await defending_player_channel.send(message)
    def check(m):
        return m.content.lower() == "confirm" and m.channel == defending_player_channel
    try:
        msg = await bot.wait_for('message', check=check, timeout=60)
    except asyncio.TimeoutError:
        await defending_player_channel.send("Confirmation time has expired")
        await ctx.send("Confirmation time has expired")
    else:
        await defending_player_channel.send("Thank you for confirming, proceeding...")
        await ctx.send("Player {} has confirmed, proceeding...".format(defending_player.name))

    #If confirmed: Calculate damage based on team effectiveness and items
    life_steal, hit_damage, damage_output_string = battle.damage_check_team(
        cur,
        attacking_player.name, attacking_player_team, 
        defending_player.name, defending_player_team
        )

    #Sending out damage calculations
    defending_player_channel.send(damage_output_string)
    ctx.send(damage_output_string)

    sql.update_player_hp(cur, attacking_player.name, life_steal)

    #Resolve damage and check for deaths
    defending_player_death = False
    defending_player_health = sql.get_player_hp(cur, defending_player.name)

    #Check for faint
    if defending_player_health <= hit_damage:
        #faint
        defending_player_death = True

        #Remove Alive Role
        masassins_alive_role = get(guild.roles(), name=settings.masassins_alive_role)
        await defending_player.remove_roles(masassins_alive_role)
        
        #Adding Faint Role
        masassins_dead_role = get(guild.roles(), name=settings.masassins_dead_role)
        await defending_player.add_roles(masassins_dead_role)

        #Set their health to zero
        sql.update_player_hp(cur, defending_player.name, (0-defending_player_health))
    else:
        sql.update_player_hp(cur, defending_player.name, (0-hit_damage))

    #Calculate reward based on whether death is true and items etc.
    total_gold_reward, total_experience_reward, total_rewards_string = battle.reward_check_player(
        cur, defending_player_death,
        attacking_player.name, attacking_player_team, 
        defending_player.name, defending_player_team
        )

    #Sending out reward strings
    ctx.send(total_rewards_string)

    #Distributing rewards
    sql.update_player_experience(cur, attacking_player.name, total_experience_reward)
    sql.update_team_experience(cur, attacking_player_team, total_experience_reward)
    sql.update_team_gold(cur, attack_player_team, total_gold_reward)

@attack.error
async def attack_error(ctx, error):
    await ctx.send(error)

@bot.command(name="hello")
async def hello(ctx):
    channel = ctx.channel
    await channel.send("Hello there!")

    def check(m):
        return m.content == "hello" and m.channel == channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=60)
    except asyncio.TimeoutError:
        await ctx.send("Timeout")
    else:
        await channel.send("Hello {.author.mention}!".format(msg))


@bot.command(name="view_players", help="View the players and their current stats")
async def view_players(ctx):
    cur = conn.cursor()
    markdown_start = "```"
    markdown_end = "```"

    newLine = "\n"
    #creation of title_string
    team_title = "Team"
    player_title = "Player"
    health_title = "Health"
    experience_title = "EXP"
    items_title = "Items"
    divider = "-" * 45

    main_string = team_title + "       " + player_title + "       " + health_title + " " + experience_title + "  " + items_title + newLine + divider + newLine
    print(main_string)
    player_rows = sql.view_players(cur).fetchall()
    for row in player_rows:
        print("Main_string:", main_string)
        team_id = row[0]
        team_name = sql.team_name_from_team_id(cur, team_id)
        main_string += team_name[:settings.length_of_team]
        length = len(team_name[:settings.length_of_team])
        main_string += " " * (settings.length_of_team - length + settings.spacing)
        
        player_name = row[1]
        length = len(player_name[:settings.length_of_name])
        main_string += player_name
        main_string += " " * (settings.length_of_name - length + settings.spacing)

        health = row[2]
        length = len(str(health))
        main_string += str(health)
        main_string += " " * (settings.length_of_health - length + settings.spacing)

        experience = row[3]
        length = len(str(experience))
        main_string += str(experience)
        main_string += " " * (settings.length_of_experience - length + settings.spacing)

        #items = row[4]
        #if len(items) > settings.length_of_items:
        #    main_string += items + newLine
        #else:
        #    main_string += items
        #    main_string += " " * (settings.length_of_items - length + settings.spacing)

        main_string += newLine

    message = markdown_start + main_string + markdown_end
    await ctx.send(message)

bot.run(token)