# massassins_bot.py
import os
from re import L
from dotenv import load_dotenv
import discord
import sqlite3
import asyncio

from discord.ext import commands
from discord.utils import get

#Local Files import
import random
import settings
import sql_functions as sql

import view_functions as view
import help_functions as f_help
import desc_functions as f_desc
import rule_functions as f_rule
import safe_zones_functions as f_safe

import Global.Locks

#Sqlite3 DB connection
conn = sqlite3.connect('masassins.db')

#Load Environment
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.load_extension("Bot.owner_commands")
bot.load_extension("Bot.admin_commands")
bot.load_extension("Bot.player_attack_command")
bot.load_extension("Bot.player_use_command")

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

@bot.command(name="desc")
async def rules(ctx):
    embed = discord.Embed(
        title = "Descriptions",
        description = "Details on important aspects of the game!",
        color = discord.Colour.teal()
    )

    for desc_command in f_desc.desc_list:
        embed.add_field(name=desc_command, value=f_desc.desc_dict[desc_command], inline=False)

    await ctx.send(embed=embed)

@bot.command(name="rule")
async def rules(ctx):
    embed = discord.Embed(
        title = "Rules",
        description = "Cheating of any kind is not permitted. You will be penalized if caught",
        color = discord.Colour.teal()
    )

    for rule_command in f_rule.rule_list:
        embed.add_field(name=rule_command, value=f_rule.rule_dict[rule_command], inline=False)

    await ctx.send(embed=embed)

@bot.command(name="safezones")
async def rules(ctx):
    embed = discord.Embed(
        title = "Safe Zones",
        description = "You can still have your privacy",
        color = discord.Colour.teal()
    )

    for safe_command in f_safe.safezone_list:
        embed.add_field(name=safe_command, value=f_safe.safezone_dict[safe_command], inline=False)

    await ctx.send(embed=embed)

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
    await Global.Locks.gold_lock.acquire()
    team_gold_amount = sql.get_team_gold(cur, team_name)
    Global.Locks.gold_lock.release()
    if team_gold_amount < settings.item_cost_dict[item_name]:
        await ctx.send("Your team does not have enough gold")
        return

    print(team_name)
    await Global.Locks.items_lock.acquire()
    if sql.get_team_item(cur,team_name,item_name) is not None:
        await ctx.send("Your team can only hold one of this item!")
        return
    Global.Locks.items_lock.release()
    #Give item to team
    await ctx.send("You have bought a {}".format(item_name))
    
    #Subtract their gold
    await Global.Locks.gold_lock.acquire()
    sql.update_team_gold(cur, team_name, (0-settings.item_cost_dict[item_name]))
    Global.Locks.gold_lock.release()
    await Global.Locks.items_lock.acquire()
    sql.give_team_item(cur, team_name, item_name)
    Global.Locks.items_lock.release()
    announcements_channel = get(guild.channels, name=settings.masassins_announcements_channel_name)

    await announcements_channel.send("Team {} has just bought a {}".format(team_name, item_name))

@buy.error
async def buy_error(ctx, error):
    await ctx.send(error)

@bot.command(name="view_all")
@commands.cooldown(1, 10, commands.BucketType.user)
async def view_all(ctx):
    cur = conn.cursor()
    for team_name in settings.team_list:
        if team_name is not settings.team_name_gym_leaders and team_name is not settings.team_name_alumni:
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