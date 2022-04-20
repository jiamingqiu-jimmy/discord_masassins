import sqlite3
import discord
from discord.ext import commands
from discord.utils import get

import settings
import sql_functions as sql

import Global.Locks

def setup(bot):
    bot.add_cog(PlayerCog(bot))
    
class PlayerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect(settings.MASASSINS_DB_NAME)

    @commands.command(name="trade_gold")
    @commands.has_role(settings.masassins_alive_role)
    async def trade_gold(self, ctx, team_name, gold_amount):
        cur = self.conn.cursor()
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

        cur = self.conn.cursor()
        await Global.Locks.gold_lock.acquire()
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
            Global.Locks.gold_lock.release()

    @trade_gold.error
    async def trade_gold_error(self, ctx, error):
        await ctx.send(error)