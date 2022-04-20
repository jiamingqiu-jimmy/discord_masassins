import sqlite3
import discord
from discord.ext import commands
from discord.utils import get

import settings
import sql_functions as sql


def setup(bot):
    bot.add_cog(AdminCog(bot))
    
class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect(settings.MASASSINS_DB_NAME)
        
    @commands.command(name="add_player")
    @commands.has_role(settings.admin_role)
    async def add_player(self, ctx, player_name, team_name):
        cur = self.conn.cursor()
        return_code = sql.insert_player(cur, player_name, team_name)
        if return_code == -1:
            await ctx.send("There has been an error, please check team_name is valid")
            return
        await ctx.send("Player {} has been added into the game, waiting for them to join".format(player_name))

    @commands.command(name="delete_player")
    @commands.has_role(settings.admin_role)
    async def delete_player(self, ctx, player_name):
        cur = self.conn.cursor()
        sql.delete_player(cur, player_name)
        await ctx.send("{} has been removed from the game".format(player_name))

    @delete_player.error
    async def delete_player_error(self, ctx, error):
        await ctx.send(error)
        
    @commands.command(name="give_player_hp")
    @commands.has_role(settings.admin_role)
    async def give_player_hp(self, ctx, player_name, hp_amount):
        cur = self.conn.cursor()        
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
    async def give_player_hp_error(self, ctx, error):
        await ctx.send(error)
        
    @commands.command(name="update_team_gold_exp")
    @commands.has_role(settings.admin_role)
    async def update_team_gold_exp(self, ctx, team_name, gold_amount, experience_amount):
        cur = self.conn.cursor()
        sql.update_team_experience(cur, team_name, experience_amount)
        sql.update_team_gold(cur, team_name, gold_amount)

        if int(gold_amount) < 0 and int(experience_amount) < 0:
            positive_gold = (0-int(gold_amount))
            positive_EXP = (0-int(experience_amount))
            sql.update_team_gold(cur, settings.team_name_gym_leaders, positive_gold)
            sql.update_team_experience(cur, settings.team_name_gym_leaders, positive_EXP)
            await ctx.send("Gym Leaders has just confiscated {} gold and {} EXP from {}".format(positive_gold, positive_EXP, team_name))
        else:
            await ctx.send("{} Gold and {} EXP changed on team {}".format(gold_amount, experience_amount, team_name))

    @update_team_gold_exp.error
    async def update_team_gold_exp_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(name="remove_item")
    @commands.has_role(settings.admin_role)
    async def remove_item(self, ctx, team_name, item_name):
        cur = self.conn.cursor()
        sql.delete_team_item(cur, team_name, item_name)
        await ctx.send("{} has been removed from team {}".format(item_name, team_name))

    @commands.command(name="give_team_experience")
    @commands.has_role(settings.admin_role)
    async def give_team_experience(self, ctx, team_name, experience_amount):
        cur = self.conn.cursor()
        sql.update_team_experience(cur, team_name, experience_amount)
        await ctx.send("{} EXP has been given to team {}".format(experience_amount, team_name))

    @commands.command(name="give_gold")
    @commands.has_role(settings.admin_role)
    async def give_gold(self, ctx, team_name, gold_amount):
        cur = self.conn.cursor()
        sql.update_team_gold(cur, team_name, gold_amount)
        await ctx.send("{} Gold has been given to the team {}".format(gold_amount, team_name))

    @commands.command(name="give_team_item")
    @commands.has_any_role(settings.admin_role)
    async def give_team_item(self, ctx, team_name, item_name):
        cur = self.conn.cursor()

        sql.give_team_item(cur, team_name, item_name)
        await ctx.send("Team {} has been given {}".format(team_name, item_name))

    @commands.command(name="change_player_team")
    @commands.has_any_role(settings.admin_role)
    async def change_team(self, ctx, player_name, team_name):
        cur = self.conn.cursor()
        #Check to make sure that the player is on a different team
        init_team_name = sql.get_player_team_name(cur, player_name)
        if team_name == init_team_name:
            await ctx.send("The player is already on your team")
            return 

        if team_name == settings.team_name_alumni:
            await ctx.send("You cannot capture an alumni with the Master Ball!")
            return
        
        if team_name == settings.team_name_gym_leaders:
            await ctx.send("You cannot capture a gym leader with the Master Ball!")
            return   
        
        #Master ball, throw master ball at a player.
        sql.update_player_team(cur, player_name, team_name)
        await ctx.send(f'{player_name}\'s team has been forcibly changed to {team_name}')
        player = get(ctx.guild.members, display_name = player_name)
        #Remove Old Team
        guild = ctx.guild
        team = get(guild.roles, name=init_team_name)
        await player.remove_roles(team)
        #Adding New Team
        new_team = get(guild.roles, name=team_name)
        await player.add_roles(new_team)
        
    @give_team_item.error
    async def give_team_item_error(self, ctx, error):
        await ctx.send(error)