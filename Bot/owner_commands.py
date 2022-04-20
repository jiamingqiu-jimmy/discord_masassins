import sqlite3
import discord
from discord.ext import commands
from discord.utils import get

import settings
import sql_functions as sql

def setup(bot):
    bot.add_cog(OwnerCog(bot))
    
class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect(settings.MASASSINS_DB_NAME)
        
    @commands.command(name="reset")
    @commands.is_owner()
    async def reset(self, ctx):
        #Creating sqlite3 db cursor
        cur = self.conn.cursor()

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
    async def reset_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(name='populate')
    @commands.is_owner()
    async def game_populate(self, ctx):
        #Creating sqlite3 db cursor
        cur = self.conn.cursor()

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
            await ctx.send("The Masassins-fainted role is created")

        masassins_alive_role = get(guild.roles, name=settings.masassins_alive_role)

        if masassins_alive_role is None:
            await ctx.send("Creating masassins-alive role...")
            masassins_alive_role = await guild.create_role(name=settings.masassins_alive_role, colour=discord.Color.dark_green())
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
        

    @commands.command(name="create_channels")
    @commands.is_owner()
    async def create_channels(self, ctx):
        await ctx.send("Creating all necessary channels...")
        guild = ctx.guild
        masassins_announcements_channel = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False)
        }
        
        masassins_channel = await guild.create_category_channel(settings.masassins_category_channel_name)
        await ctx.send("Created Category Channel")

        all_team_channel_overwrite = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True)
        }
        announcements_channel_name = await masassins_channel.create_text_channel(name=settings.masassins_announcements_channel_name, overwrites=masassins_announcements_channel, position=0)
        await ctx.send("Created Announcements Channel")
        
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

    @commands.command(name="delete_channels")
    @commands.is_owner()
    async def delete_channels(self, ctx):
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
