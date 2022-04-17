# massassins_bot.py
import os
from dotenv import load_dotenv
import discord
import sqlite3
import asyncio

from discord.ext import commands
from discord.utils import get

#Local Files import
import settings
import sql_functions as sql
import battle_functions as battle
import view_functions as view
import help_functions as f_help

#Sqlite3 DB connection
conn = sqlite3.connect('masassins.db')

#Load Environment
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
client = discord.Client()
bot.remove_command('help')

@bot.event
async def on_ready():
    print('{} has connected to Discord!'.format(bot.user.name))

@bot.command(name="help")
async def help(ctx):
    embed = discord.Embed(
        title = "Functions Academy",
        description = "List of functions and their use",
        color = discord.Colour.teal()
    )

    for help_command in f_help.list_of_help:
        embed.add_field(name=help_command, value=f_help.help_dict[help_command], inline=False)

    await ctx.send(embed=embed)

@bot.command(name='reset')
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

@bot.command(name='populate')
@commands.is_owner()
async def game_populate(ctx):
    #Creating sqlite3 db cursor
    cur = conn.cursor()

    #Populating pre-set items and teams
    await ctx.send("Processing teams and items...")
    sql.insert_teams(cur, settings.team_list)
    sql.insert_items(cur, settings.item_dict)

    guild = ctx.guild
    masassins_dead_role = get(guild.roles, name=settings.masassins_dead_role)
    #Creating all the necessary roles
    if masassins_dead_role is None:
        await ctx.send("Creating masassins-fainted role...")
        masassins_dead_role = await guild.create_role(name=settings.masassins_dead_role, colour=discord.Color.dark_orange())
        masassins_dead_role.color = discord.Color.dark_orange()
        await ctx.send("The Masassins-fainted role is created")

    masassins_alive_role = get(guild.roles, name=settings.masassins_alive_role)

    if masassins_alive_role is None:
        await ctx.send("Creating masassins-alive role...")
        masassins_alive_role = await guild.create_role(name=settings.masassins_alive_role, colour=discord.Color.dark_green())
        masassins_alive_role.color = discord.Color.dark_green()
        await ctx.send("The Massassins-alive role is created")

    masassins_admin_role = get(guild.roles, name=settings.admin_role)

    if masassins_admin_role is None:
        await ctx.send("Creating masassins-admin role...")
        masassins_admin_role = await guild.create_role(name=settings.admin_role, hoist=True, colour=discord.Color.dark_gold())
        await ctx.send("The masassins-admin role is created")

    for player_name in settings.admins_list:
        admin_player = get(guild.members, display_name=player_name)
        if admin_player is not None:
            await admin_player.add_roles(masassins_admin_role)

    for team_name in settings.team_list:
        team_role = get(guild.roles, name=team_name)
        if team_role is None:
            await ctx.send("Creating new team role {} ...".format(team_name))
            team_role = await guild.create_role(name=team_name, hoist=True)
            await ctx.send("The Team Role {} is created".format(team_name))

    #Processing the players
    await ctx.send("Finished processing teams and items, now processing players")
    for player_name,player_team_name in settings.player_team_dict.items():
        return_code = sql.insert_player(cur, player_name, player_team_name)
        if return_code == -1:
            await ctx.send('There has been an error processing team_name, double-check hard-coded team names in player-team-dict')
        else:
            await ctx.send("{} has been processed...".format(player_name))
    await ctx.send("All players has been processed, waiting for players to join...")

@bot.command(name="add_player")
@commands.has_role(settings.admin_role)
async def add_player(ctx, player_name, team_name):
    return_code = sql.insert_player(cur, player_name, team_name)
    if return_code == -1:
        await ctx.send("There has been an error, please check team_name is valid")
        return
    await ctx.send("Player {} has been added into the game, waiting for them to join".format(player_name))

@bot.command(name="trade_gold")
@commands.has_role(settings.masassins_alive_role)
async def trade_gold(ctx, team_name, gold_amount):
    cur = conn.cursor()
    guild = ctx.guild
    player_name = ctx.author.display_name

    if int(gold_amount) < 1:
        await ctx.send("You cannot trade 0 or negative gold")
        return

    if team_name not in settings.team_list:
        await ctx.send("That is not a valid team, please check team name")
        return

    #Init_player_team_name
    init_player_team_name = sql.get_player_team_name(cur, player_name)

    cur = conn.cursor()
    lock = asyncio.Lock()
    await lock.acquire()
    try:
        team_gold_amount = sql.get_team_gold(cur, init_player_team_name)
        if int(team_gold_amount) < int(gold_amount):
            await ctx.send("Your team does not have that much gold to trade!")
            return
        sql.update_team_gold(cur, init_player_team_name, int(0-int(gold_amount)))
        sql.update_team_gold(cur, team_name, int(gold_amount))
        announcements_channel = get(guild.channels, name=settings.masassins_announcements_channel_name)
        await announcements_channel.send("{} has given {} gold to {}".format(init_player_team_name, gold_amount, team_name))
        await ctx.send("{} has given {} gold to {}".format(init_player_team_name, gold_amount, team_name))
    except:
        await ctx.send("An error has occured! Please check to make sure nothing changed and try again!")
    finally:
        lock.release()

@trade_gold.error
async def trade_gold_error(ctx, error):
    await ctx.send(error)

@bot.command(name="remove_item")
@commands.has_role(settings.admin_role)
async def remove_item(ctx, team_name, item_name):
    cur = conn.cursor()
    sql.delete_team_item(cur, team_name, item_name)
    await ctx.send("{} has been removed from team {}".format(item_name, team_name))

@bot.command(name="give_team_experience")
@commands.has_role(settings.admin_role)
async def give_team_experience(ctx, team_name, experience_amount):
    cur = conn.cursor()
    sql.update_team_experience(cur, team_name, experience_amount)
    await ctx.send("{} EXP has been given to team {}".format(experience_amount, team_name))

@bot.command(name="give_gold")
@commands.has_role(settings.admin_role)
async def give_gold(ctx, team_name, gold_amount):

    cur = conn.cursor()
    sql.update_team_gold(cur, team_name, gold_amount)
    await ctx.send("{} Gold has been given to the team {}".format(gold_amount, team_name))

@bot.command(name="update_team_gold_exp")
@commands.has_role(settings.admin_role)
async def update_team_gold_exp(ctx, team_name, gold_amount, experience_amount):
    cur = conn.cursor()
    sql.update_team_experience(cur, team_name, experience_amount)
    sql.update_team_gold(cur, team_name, gold_amount)
    
    if int(gold_amount) < 0 and int(experience_amount) < 0:
        positive_gold = (0-int(gold_amount))
        positive_EXP = (0-int(experience_amount))
        sql.update_team_gold(cur, settings.team_name_team_rocket, positive_gold)
        sql.update_team_experience(cur, settings.team_name_team_rocket, positive_EXP)
        await ctx.send("Team Rocket has just stolen {} gold and {} EXP from {}".format(positive_gold, positive_EXP, team_name))
    else:
        await ctx.send("{} Gold and {} EXP changed on team {}".format(gold_amount, experience_amount, team_name))

@update_team_gold_exp.error
async def update_team_gold_exp_error(ctx, error):
    await ctx.send(error)

@bot.command(name="give_player_hp")
@commands.has_role(settings.admin_role)
async def give_player_hp(ctx, player_name, hp_amount):
    cur = conn.cursor()        
    guild = ctx.guild
    target_player = get(guild.members, display_name=player_name)
    #Check that the target_player is dead
    masassins_dead_role = get(target_player.roles, name=settings.masassins_dead_role)
    if masassins_dead_role is not None:
        await ctx.send("Revived {}!".format(player_name))
        await target_player.remove_roles(masassins_dead_role)
        masassins_alive_role = get(guild.roles, name=settings.masassins_alive_role)
        await target_player.add_roles(masassins_alive_role)       

    sql.update_player_hp(cur, player_name, hp_amount)
    await ctx.send("{} HP has been given to player {}".format(hp_amount, player_name))

@give_player_hp.error
async def give_player_hp_error(ctx, error):
    await ctx.send(error)

@bot.command(name="delete_player")
@commands.has_role(settings.admin_role)
async def delete_player(ctx, player_name):
    cur = conn.cursor()
    sql.delete_player(cur, player_name)
    await ctx.send("{} has been removed from the game".format(player_name))

@delete_player.error
async def delete_palyer_error(ctx, error):
    await ctx.send(error)

@bot.command(name="create_channels")
@commands.is_owner()
async def create_channels(ctx):
    await ctx.send("Creating all necessary channels...")
    guild = ctx.guild
    masassins_announcements_channel = {
        guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False)
    }
    announcements_channel_name = await guild.create_text_channel(name=settings.masassins_announcements_channel_name, overwrites=masassins_announcements_channel, position=0)
    await ctx.send("Created Announcements Channel")

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
        staff_role = get(guild.roles, name=settings.MASA_staff_role)
        team_channel_overwrite = {
            admin_role: discord.PermissionOverwrite(read_messages=True),
            team_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            staff_role: discord.PermissionOverwrite(read_messages=False)
        }
        await masassins_channel.create_text_channel(name=team_name, overwrites=team_channel_overwrite)
        await ctx.send("Created {} Discussion Channel".format(team_name))
    
    await ctx.send("All Done!")

@bot.command(name="delete_channels")
@commands.is_owner()
async def delete_channels(ctx):
    guild = ctx.guild

    channels_list = guild.channels
    for channel in channels_list:
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

@bot.command(name="join")
async def join(ctx):
    cur = conn.cursor()
    player_display_name = ctx.author.display_name
    guild = ctx.guild
    await ctx.send("Hello {} please wait while we process your join request".format(player_display_name))
    if sql.valid_player_check(cur, player_display_name) == 0:
        team_name = sql.get_player_team_name(cur, player_display_name)

        member = ctx.message.author
        guild = member.guild

        masassins_alive_role = get(guild.roles, name=settings.masassins_alive_role)
        team_role = get(guild.roles, name=team_name)
        if get(member.roles, name=team_name) is not None:
            await ctx.send("You already joined the game")
            return

        await member.add_roles(masassins_alive_role)
        await member.add_roles(team_role)
        await ctx.send("Hello {}, we found your name in our database so you will now be given your team and corresponding roles".format(player_display_name))
        await ctx.send("Hello {}, your team is {}".format(player_display_name, team_role))
    else:
        await ctx.send("Sorry your name was not found, please contact the admins")

@join.error
async def join_error(ctx, error):
    await ctx.send(error)

@bot.command(name='use')
@commands.has_any_role(settings.admin_role, settings.masassins_alive_role)
async def use(ctx, item_name, player_name):
    cur = conn.cursor()
    init_player = ctx.author
    init_player_name = ctx.author.display_name
    guild = ctx.guild

    #Init_player_team_name
    init_player_team_name = sql.get_player_team_name(cur, init_player_name)

    if player_name is None or sql.valid_player_check(cur, player_name) != 0:
        await ctx.send("Please check to make sure the player name is correct, capitalization does matter")
        return

    #Get the player's current team
    team_name = sql.get_player_team_name(cur, player_name)

    #Check to see if the team listed is the player's team
    if (init_player_team_name != team_name):
        await ctx.send("Item must be used on a player in the same team. Function is !use <item_name> <player_name>")
        return

    #Check to see if it is a valid item
    if (sql.valid_item_check(cur, item_name) != 0):
        await ctx.send("Please check that the item name is correct")
        return


    #Check to see if the current team owns the item
    if sql.get_team_item(cur, init_player_team_name, item_name) is None:
        await ctx.send("Your team does not currently own this item")
        return

    target_player = get(guild.members, display_name=player_name)
    if target_player is None:
        await ctx.send("This player is not part of the game")
        return

    #Map the item to a specific item and effect
    if item_name == settings.item_name_potion:
        player_health = sql.get_player_hp(cur, player_name)

        max_player_hp = settings.max_player_hp
        if player_health == max_player_hp:
            await ctx.send("Player is already at max health! You cannot use a potion on him")
            return
        elif player_health > (max_player_hp - settings.potion_healing):
            await ctx.send("You have used a potion! You healed to full by gaining {} health!".format(max_player_hp - player_health))
            sql.update_player_hp(cur, player_name, (max_player_hp - player_health))
        else:
            sql.update_player_hp(cur, player_name, settings.potion_healing)
            await ctx.send("You have used a potion! you have gained {} health".format(settings.potion_healing))
    
        sql.delete_team_item(cur, team_name, item_name)

    elif item_name == settings.item_name_revive:
        #Check that the target_player is dead
        masassins_dead_role = get(target_player.roles, name=settings.masassins_dead_role)
        if masassins_dead_role is None:
            await ctx.send("Target player is not fainted, you cannot use revive on them")
            return
        await target_player.remove_roles(masassins_dead_role)

        masassins_alive_role = get(guild.roles, name=settings.masassins_alive_role)
        await target_player.add_roles(masassins_alive_role)       
        sql.update_player_hp(cur, player_name, settings.revive_healing)
        await ctx.send("{} has been given revive. He has been revived!".format(player_name))
        sql.delete_team_item(cur, team_name, item_name)

    elif item_name == settings.item_name_sitrus_berry:
        #Check to make sure the player does not already have the item
        if sql.get_player_item(cur, player_name, item_name) is not None:
            await ctx.send("The player already has that item")
            return

        #Sitrus berry, give sitrus berry to a player
        sql.give_player_item(cur, player_name, item_name)
        await ctx.send("{} has been given sitrus berry. They are invulnerable for 1 hour!".format(player_name))
        #Remove item from team
        sql.delete_team_item(cur, team_name, item_name)

    elif item_name == settings.item_name_master_ball:
        #Check to make sure that the player is on a different team
        new_team_name = sql.get_player_team_name(curr, init_player_name)
        if new_team_name == team_name:
            await ctx.send("The player is already on your team")
            return 

        #Master ball, throw master ball at a player.
        sql.update_player_team(cur, player_name, new_team_name)
        await ctx.send("{} has been caught by a master ball".format(player_name))
        #Remove item from team
        sql.delete_team_item(cur, team_name, item_name)
    
    elif item_name == settings.item_name_poke_ball:
        #Check to make sure the player is not already in the game
        if sql.valid_player_check(cur, player_name) == 0:
            await ctx.send("The player is already in the game)
            return
        
        #Poke ball, throw poke ball at a new player
        sql.insert_player(cur, player_name)
        await ctx.send("{} has been caught by a poke ball".format(player_name))
        #Remove item from team
        sql.delete_item_from_team(cur, team_name, item_name)

    elif item_name == settings.item_name_focus_sash:
        #Check to make sure the player does not already have the item
        if sql.get_player_item(cur, player_name, item_name) is not None:
            await ctx.send("The player already has that item")
            return

        #Focus sash, give focus sash to a player
        sql.give_player_item(cur, player_name, item_name)
        await ctx.send("{} has been given focus sash".format(player_name))
        #Remove item from team
        sql.delete_team_item(cur, team_name, item_name)

    else:
        await ctx.send("You cannot give that item to a player")

@use.error
async def use_an_item_error(ctx,error):
    await ctx.send(error)

@bot.command(name="attack")
@commands.has_any_role(settings.admin_role, settings.masassins_alive_role)
@commands.cooldown(1, 30, commands.BucketType.user)
async def attack(ctx, player_name): #Maybe consider instead of inputting names, use mention
    cur = conn.cursor()
    guild = ctx.guild
    attacking_player = ctx.author
    attacking_player_name = ctx.author.display_name
    defending_player = get(ctx.guild.members, display_name=player_name)
    defending_player_name = defending_player.display_name

    #Check for a valid player in the database
    if defending_player is None or sql.valid_player_check(cur, defending_player_name) != 0 :
        await ctx.send("Please check that you have the right player (capitalization matters), the command is !attack <player_name>")
        return 

    #Send message into the player's team channel asking for confirmation use @mention
    defending_player_team = sql.get_player_team_name(cur, defending_player_name)
    attacking_player_team = sql.get_player_team_name(cur, attacking_player_name)

    defending_player_channel = get(guild.text_channels, name=defending_player_team.lower())

    if defending_player_team.lower() == attacking_player_team.lower():
        await ctx.send("You cannot attack players from the same team!")
        return

    #Check to make sure that the player has joined the game
    defending_player_masassins_role = get(defending_player.roles, name=settings.masassins_alive_role)
    if defending_player_masassins_role is None:
        await ctx.send("You cannot attack this player who hasn't officially joined the game yet!")
        return

    #Check to make sure that the attacking player has joined the game
    attacking_player_masassins_role = get(attacking_player.roles, name=settings.masassins_alive_role)
    if attacking_player_masassins_role is None:
        await ctx.send("You cannot attack this player when you haven't officially joined the game yet!")

    #Wait for confirmation, 25 second deadline or auto-cancel
    message = """
        Hello team {}, {} has just initiated a hit on {}. 
        {} you have 25 seconds to confirm otherwise hit will be cancelled. Type in CONFIRM to confirm the hit """
    message = message.format(defending_player_team, attacking_player_name, defending_player_name, defending_player.mention)
    await defending_player_channel.send(message)
    def check(m):
        return m.content.lower() == "confirm" and m.channel == defending_player_channel and m.author.display_name == defending_player_name
    try:
        msg = await bot.wait_for('message', check=check, timeout=25)
    except asyncio.TimeoutError:
        await defending_player_channel.send("Confirmation time has expired")
        await ctx.send("Confirmation time has expired")
        return
    else:
        await defending_player_channel.send("Thank you for confirming, proceeding...")
        await ctx.send("Player {} has confirmed, proceeding...".format(defending_player_name))


    #If confirmed: Calculate damage based on team effectiveness and items
    life_steal, hit_damage, damage_output_list = battle.damage_check_team(
        cur,
        attacking_player_name, attacking_player_team, 
        defending_player_name, defending_player_team
        )

    player_health = sql.get_player_hp(cur, attacking_player_name)
    if player_health != settings.max_player_hp:
        if player_health > (settings.max_player_hp - settings.shell_bell_hit_healing ):
            sql.update_player_hp(cur, attacking_player_name, (settings.max_player_hp - settings.shell_bell_hit_healing))
        else:
            sql.update_player_hp(cur, attacking_player_name, life_steal)

    #Resolve damage and check for deaths
    defending_player_death = False
    defending_player_health = sql.get_player_hp(cur, defending_player_name)

    #Check for faint
    if defending_player_health <= hit_damage:
        #faint
        defending_player_death = True

        #Remove Alive Role
        masassins_alive_role = get(guild.roles, name=settings.masassins_alive_role)
        await defending_player.remove_roles(masassins_alive_role)
        
        #Adding Faint Role
        masassins_dead_role = get(guild.roles, name=settings.masassins_dead_role)
        await defending_player.add_roles(masassins_dead_role)

        sql.delete_player_items(cur, defending_player_name)
        #Set their health to zero
        sql.update_player_hp(cur, defending_player_name, (0-defending_player_health))
    else:
        sql.update_player_hp(cur, defending_player_name, (0-hit_damage))

    #Calculate reward based on whether death is true and items etc.
    total_gold_reward, total_experience_reward, total_rewards_list = battle.reward_check_player(
        cur, defending_player_death,
        attacking_player_name, attacking_player_team, 
        defending_player_name, defending_player_team
        )

    attack_situation_string = ""
    if defending_player_death:
        attack_situation_string = "fainted "
    else:
        attack_situation_string = "hit "

    embed = discord.Embed(
        title = attacking_player_name + " ({}) ".format(attacking_player_team) + attack_situation_string + defending_player_name + " ({}) ".format(defending_player_team),
        colour = discord.Colour.orange()
    )

    attacking_health = sql.get_player_hp(cur, attacking_player_name)
    defending_health = sql.get_player_hp(cur, defending_player_name)

    damage_output_list.append("----- Remaining HP -----")
    damage_output_list.append("{} HP : {}".format(attacking_player_name, attacking_health))
    damage_output_list.append("{} HP : {}".format(defending_player_name, defending_health))

    damage_calculations_string = ""
    for calc in damage_output_list:
        damage_calculations_string += calc + "\n"

    rewards_calculations_string = ""
    for reward in total_rewards_list:
        rewards_calculations_string += reward + "\n"

    embed.add_field(name="Damage Calculations", value=damage_calculations_string, inline=False)
    embed.add_field(name="Reward Calculations", value=rewards_calculations_string, inline=False)


    #Distributing rewards
    sql.update_player_experience(cur, attacking_player_name, total_experience_reward)
    sql.update_team_experience(cur, attacking_player_team, total_experience_reward)
    sql.update_team_gold(cur, attacking_player_team, total_gold_reward)

    attacking_team_gold, attacking_team_exp = sql.get_teams(cur, attacking_player_team)
    attacking_team_values = "Gold : {} \nEXP: {}".format(attacking_team_gold, attacking_team_exp)
    embed.add_field(name="{} Resulting Team Gold/EXP".format(attacking_player_team), value=attacking_team_values, inline=False)

    announcements_channel = get(guild.channels, name=settings.masassins_announcements_channel_name)
    await announcements_channel.send(embed=embed)
    await ctx.send(embed=embed)

@attack.error
async def attack_error(ctx, error):
    await ctx.send(error)

@bot.command(name="hello")
async def hello(ctx):
    channel = ctx.channel
    await channel.send("Hello there {}!".format(ctx.author.display_name))

    def check(m):
        return m.content == "hello" and m.channel == channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=60)
    except asyncio.TimeoutError:
        await ctx.send("Timeout")
    else:
        await channel.send("Hello {.author.mention}!".format(msg))

@bot.command(name="shop")
@commands.has_any_role(settings.admin_role, settings.masassins_alive_role)
async def pokemart(ctx):
    embed = discord.Embed(
        title="Poke Mart",
        description = "You can buy items here!",
        colour = discord.Colour.blue()
    )

    for item_name in settings.item_list:
        item_cost = 0
        title_name = 0

        if item_name == settings.item_name_expshare:
            title_name = item_name + " - Out of Stock "
        else:
            item_cost = " - {} gold".format(settings.item_cost_dict[item_name])
            title_name = item_name + item_cost
        
        embed.add_field(name=title_name,value=settings.item_dict[item_name],inline=False)

    await ctx.send(embed=embed)

@bot.command(name="buy")
@commands.has_any_role(settings.admin_role, settings.masassins_alive_role)
async def buy(ctx, *args):
    cur = conn.cursor()
    player = ctx.author
    guild = ctx.guild
    player_name = ctx.author.display_name
    team_name = sql.get_player_team_name(cur, player_name)
    item_name = " ".join(args[:])
    print(item_name)

    #Check if it is a valid item
    if sql.valid_item_check(cur, item_name) != 0:
        await ctx.send("Please check that the item name you inputted is correct")
        return

    #Check if the team has enough gold to buy it
    team_gold_amount = sql.get_team_gold(cur, team_name)
    if team_gold_amount < settings.item_cost_dict[item_name]:
        await ctx.send("Your team does not have enough gold")
        return

    if sql.get_team_item(cur,team_name,item_name) is not None:
        await ctx.send("Your team can only hold one of this item!")
        return

    #Give item to team
    await ctx.send("You have bought a {}".format(item_name))
    
    #Subtract their gold
    sql.update_team_gold(cur, team_name, (0-settings.item_cost_dict[item_name]))

    sql.give_team_item(cur, team_name, item_name)
    announcements_channel = get(guild.channels, name=settings.masassins_announcements_channel_name)

    await announcements_channel.send("Team {} has just bought a {}".format(team_name, item_name))

@buy.error
async def buy_error(ctx, error):
    await ctx.send(error)

@bot.command(name="give_team_item")
@commands.has_any_role(settings.admin_role)
async def give_team_item(ctx, team_name, item_name):
    cur = conn.cursor()

    sql.give_team_item(cur, team_name, item_name)
    await ctx.send("Team {} has been given {}".format(team_name, item_name))

@give_team_item.error
async def give_team_item_error(ctx, error):
    await ctx.send(error)

@bot.command(name="view_all")
@commands.cooldown(1, 10, commands.BucketType.user)
async def view_all(ctx):
    cur = conn.cursor()
    for team_name in settings.team_list:
        if team_name is not settings.team_name_team_rocket and team_name is not settings.team_name_alumni:
            await view.view_team(cur, ctx, team_name)

@bot.command(name="v")
async def v(ctx, team_name):
    cur = conn.cursor()
    for name in settings.team_list:
        if name.lower() == team_name.lower():
            await view.view_team(cur, ctx, team_name)
            return
    await ctx.send("Team name not found, double check your team name input")

@v.error
async def v_error(ctx, error):
    await ctx.send(error)

bot.run(token)