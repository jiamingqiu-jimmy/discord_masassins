import sqlite3
import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import random
import settings
import sql_functions as sql
import battle_functions as battle

def setup(bot):
    bot.add_cog(PlayerUseCog(bot))
    
class PlayerUseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect(settings.MASASSINS_DB_NAME)


    @commands.command(name='use')
    @commands.has_any_role(settings.admin_role, settings.masassins_alive_role)
    async def use(self, ctx, item_name, player_name):
        cur = self.conn.cursor()
        init_player = ctx.author
        init_player_name = ctx.author.display_name
        guild = ctx.guild

        #Init_player_team_name
        init_player_team_name = sql.get_player_team_name(cur, init_player_name)
        
        team_name = str
        
        if player_name is None:
            await ctx.send("Please check to make sure the player name is correct, capitalization does matter")
            return
        
        if item_name != settings.item_name_poke_ball:
            if player_name is None or sql.valid_player_check(cur, player_name) != 0:
                await ctx.send("Please check to make sure the player name is correct, capitalization does matter")
                return

            #Get the player's current team
            team_name = sql.get_player_team_name(cur, player_name)

        #Check to see if it is a valid item
        if (sql.valid_item_check(cur, item_name) != 0):
            await ctx.send("Please check that the item name is correct")
            return

        #Check to see if the current team owns the item
        if sql.get_team_item(cur, init_player_team_name, item_name) is None:
            await ctx.send("Your team does not currently own this item")
            return

        #Map the item to a specific item and effect
        if item_name == settings.item_name_potion:
            #Check to see if the team listed is the player's team
            if (init_player_team_name != team_name):
                await ctx.send("Item must be used on a player in the same team. Function is !use <item_name> <player_name>")
                return
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
            target_player = get(guild.members, display_name=player_name)

            if target_player is None:
                await ctx.send("This player is not part of the game")
                return
        
            #Check to see if the team listed is the player's team
            if (init_player_team_name != team_name):
                await ctx.send("Item must be used on a player in the same team. Function is !use <item_name> <player_name>")
                return
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

        elif item_name == settings.item_name_master_ball:
            #Check to make sure that the player is on a different team
            new_team_name = sql.get_player_team_name(cur, init_player_name)
            if new_team_name == team_name:
                await ctx.send("The player is already on your team")
                return 

            if team_name == settings.team_name_alumni:
                await ctx.send("You cannot capture an alumni with the Master Ball!")
                return
            
            if team_name == settings.team_name_gym_leaders:
                await ctx.send("You cannot capture a gym leader with the Master Ball!")
                return   
            
            #Master ball, throw master ball at a player.
            sql.update_player_team(cur, player_name, new_team_name)
        
            player = get(ctx.guild.members, display_name = player_name)
            #Remove Old Team
            team = get(guild.roles, name=team_name)
            await player.remove_roles(team)
            #Adding New Team
            new_team = get(guild.roles, name=new_team_name)
            await player.add_roles(new_team)
            await ctx.send("{} has been caught by a master ball".format(player_name))
            #Remove item from team
            sql.delete_team_item(cur, new_team_name, item_name)
        
        elif item_name == settings.item_name_gacha_ball:
            #Check to make sure that the player is on a different team
            new_team_name = sql.get_player_team_name(cur, init_player_name)
            if new_team_name == team_name:
                await ctx.send("The player is already on your team")
                return 
            
            if team_name == settings.team_name_alumni:
                await ctx.send("You cannot capture an alumni with the Gacha Ball!")
                return
            
            if team_name == settings.team_name_gym_leaders:
                await ctx.send("You cannot capture a gym leader with the Gacha Ball!")
                return 

            #gacha ball, throw gacha ball at a player.
            catch = random.uniform(0,1)
            if catch >= settings.gacha_ball_catch_chance:
                await ctx.send("{} got away...".format(player_name))
            else:
                sql.update_player_team(cur, player_name, new_team_name)
                
                player = get(ctx.guild.members, display_name = player_name)
                #Remove Old Team
                team = get(guild.roles, name=team_name)
                await player.remove_roles(team)
                #Adding New Team
                new_team = get(guild.roles, name=new_team_name)
                await player.add_roles(new_team)
                await ctx.send("{} has been caught by a gacha ball".format(player_name))
            #Remove item from team
            sql.delete_team_item(cur, new_team_name, item_name)
        elif item_name == settings.item_name_poke_ball:
            print("Pokeball!")
            #Check to make sure the player is not already in the game
            if sql.valid_player_check(cur, player_name) == 0:
                await ctx.send("The player is already in the game")
                return
            
            #Poke ball, throw poke ball at a new player
            sql.insert_player(cur, player_name, init_player_team_name)
            
            player = get(ctx.guild.members, display_name = player_name)
            
            #Add to team
            team = get(guild.roles, name=init_player_team_name)
            masassins_alive_role = get(guild.roles, name=settings.masassins_alive_role)
            await player.add_roles(team)
            await player.add_roles(masassins_alive_role)
            await ctx.send("{} has been caught by a poke ball".format(player_name))
            await ctx.send("{} is joining Team {}".format(player_name, init_player_team_name))
            
            announcements_channel = get(guild.channels, name=settings.masassins_announcements_channel_name)
            await announcements_channel.send("{} has been caught by a pokeball from Team {}".format(player_name, init_player_team_name))
            
            #Remove item from team
            sql.delete_team_item(cur, init_player_team_name, item_name)

        else:
            await ctx.send("You cannot give that item to a player")

    @use.error
    async def use_an_item_error(self, ctx, error):
        await ctx.send("The use command is : use <item-name> <player-name>")
        await ctx.send(error)