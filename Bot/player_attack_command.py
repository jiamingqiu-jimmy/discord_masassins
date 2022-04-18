import sqlite3
import discord
from discord.ext import commands
from discord.utils import get
import asyncio

import settings
import sql_functions as sql
import battle_functions as battle

import Global.Locks

def setup(bot):
    bot.add_cog(PlayerAttackCog(bot))
    
class PlayerAttackCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect(settings.MASASSINS_DB_NAME)

    @commands.command(name="attack")
    @commands.has_any_role(settings.admin_role, settings.masassins_alive_role)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def attack(self, ctx, player_name): #Maybe consider instead of inputting names, use mention
        cur = self.conn.cursor()
        guild = ctx.guild
        attacking_player = ctx.author
        attacking_player_name = ctx.author.display_name
        ctx.guild.fetch_members()
        
        defending_player = get(ctx.guild.members, display_name = player_name)
        
        defending_player_name = defending_player.display_name

        #Check for a valid player in the database
        if defending_player is None or sql.valid_player_check(cur, defending_player_name) != 0 :
            await ctx.send("Please check that you have the right player (capitalization matters), the command is !attack <player_name>")
            return

        #Send message into the player's team channel asking for confirmation use @mention
        defending_player_team = sql.get_player_team_name(cur, defending_player_name)
        attacking_player_team = sql.get_player_team_name(cur, attacking_player_name)

        print(guild.text_channels)
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
            msg = await self.bot.wait_for('message', check=check, timeout=25)
        except asyncio.TimeoutError:
            await defending_player_channel.send("Confirmation time has expired")
            await ctx.send("Confirmation time has expired")
            return
        else:
            await defending_player_channel.send("Thank you for confirming, proceeding...")
            await ctx.send("Player {} has confirmed, proceeding...".format(defending_player_name))


        #If confirmed: Calculate damage based on team effectiveness and items
        hit_damage, damage_output_list = battle.damage_check_team(
            cur,
            attacking_player_name, attacking_player_team, 
            defending_player_name, defending_player_team
            )

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
            await Global.Locks.items_lock.acquire()
            sql.delete_player_items(cur, defending_player_name)
            Global.Locks.items_lock.release()
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
        await Global.Locks.gold_lock.acquire()
        sql.update_team_gold(cur, attacking_player_team, total_gold_reward)

        attacking_team_gold = sql.get_team_gold(cur, attacking_player_team)
        attacking_team_exp = sql.get_team_experience(cur, attacking_player_team)
        attacking_team_values = "Gold : {} \nEXP: {}".format(attacking_team_gold, attacking_team_exp)
        Global.Locks.gold_lock.release()
        embed.add_field(name="{} Resulting Team Gold/EXP".format(attacking_player_team), value=attacking_team_values, inline=False)

        attacking_player_values = "EXP: {}".format(sql.get_player_experience(cur, attacking_player_name))
        embed.add_field(name="{}'s Resulting EXP".format(attacking_player_name), value=attacking_player_values, inline=False)
        
        announcements_channel = get(guild.channels, name=settings.masassins_announcements_channel_name)
        await announcements_channel.send(embed=embed)
        await ctx.send(embed=embed)

    @attack.error
    async def attack_error(ctx, error):
        await ctx.send(error)