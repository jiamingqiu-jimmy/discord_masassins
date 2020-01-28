import settings
import sql_functions as sql
import sqlite3
import discord


async def view_team(cur, ctx, team_name):
    for team_n in settings.team_list:
        if team_n.lower() == team_name.lower():
            team_name = team_n
    
    player_rows = sql.view_players(cur, team_name)
    if len(player_rows) != 0:

        name_string = ""
        health_exp_string = ""
        player_items_string = ""
        team_items_string = ""
        for player_row in player_rows:
            player_name = player_row[0]
            name_string += player_name + "\n"
            health_exp_string += str(player_row[1]) + " / " + str(player_row[2]) + "\n"
            items_string = ""
            for item_name in settings.item_list:
                if sql.find_player_item(cur, player_name, item_name) is not None:
                    items_string += item_name + " - "

            if items_string == "":
                player_items_string += "no items\n"
            else:
                player_items_string += items_string + "\n"

        team_gold, team_experience = sql.view_teams(cur, team_name)
        team_items = sql.view_team_items(cur, team_name)
        for item_row in team_items:
            item_count = sql.view_team_item_count(cur, team_name, item_row[0])
            team_items_string += item_row[0] + "({})".format(item_count[0]) + " "
        
        embed = discord.Embed(
            title = team_name,
            description = "Gold: {}  -  EXP: {}\nTeam-Items: {}".format(team_gold, team_experience, team_items_string),
            color = discord.Colour.blue()
        )
        
        if items_string == "":
            items_string = "no items"
        embed.add_field(name="Name", value=name_string, inline=True)
        embed.add_field(name="Health/EXP", value=health_exp_string, inline=True)
        embed.add_field(name="Items", value=player_items_string, inline=True)
        await ctx.send(embed=embed)