#test.py

import os
import sqlite3
import sql_functions as sql
import settings

conn = sqlite3.connect('test.db')

cur = conn.cursor()

sql.drop_tables(cur)
sql.create_tables(cur)
sql.populate_items_table( cur, settings.item_dict )
sql.populate_teams_table( cur, settings.team_list )
sql.view_teams_list(cur)
for player_name,team_name in settings.player_team_dict.items():
    return_code = sql.valid_team_check(cur, team_name)
    if return_code != 0:
        print("Errror!!!!", return_code)
    sql.populate_players_table(cur, player_name, team_name)
    print("Player Name :", player_name, " : ", "Team Name : ", team_name)