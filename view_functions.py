import settings
import sql_functions as sql
import sqlite3
import discord


async def view_team(cur, ctx, team_name):
    for team_n in settings.team_list:
        if team_n.lower() == team_name.lower():
            team_name = team_n
    
    player_rows = sql.get_players_from_team(cur, team_name)
    if len(player_rows) != 0:

        player_string = ""
        for player_row in player_rows:
            player_name = player_row[0]
            player_string += player_name + " - "
            player_string += str(player_row[1]) + " / " + str(player_row[2]) + " - "
            for item_name in settings.item_list:
                if sql.get_player_item(cur, player_name, item_name) is not None:
                    player_string += item_name + " - "
            player_string += "\n"

        team_items_string = ""
        team_gold = sql.get_team_gold(cur, team_name)
        team_experience = sql.get_team_experience(cur, team_name)
        team_items = sql.get_team_items(cur, team_name)
        
        for item_row in team_items:
            item_count = sql.get_team_item_count(cur, team_name, item_row[0])
            team_items_string += item_row[0] + "({})".format(item_count) + " "
        
        embed = discord.Embed(
            title = team_name,
            description = "Gold: {}  -  EXP: {}\nTeam-Items: {}".format(team_gold, team_experience, team_items_string),
            color = discord.Colour.blue()
        )
        
        embed.add_field(name="Name - Health/Exp - Items(etc..)", value=player_string, inline=True)

        await ctx.send(embed=embed)