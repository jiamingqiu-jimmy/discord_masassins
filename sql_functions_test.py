import sqlite3
import settings
import pytest
import sql_functions as sql


def test_simple():
    conn = sqlite3.connect('SQLTEST.db')
    cur = conn.cursor()
    sql.create_tables(cur)
    sql.insert_items( cur, settings.item_dict )
    sql.insert_teams( cur, settings.team_list )
    for player_name,team_name in settings.player_team_dict.items():
        return_code = sql.valid_team_check(cur, team_name)
        if return_code != 0:
            print("Errror!!!!", return_code)
        sql.insert_player(cur, player_name, team_name)
        print("Player Name :", player_name, " : ", "Team Name : ", team_name)
    sql.update_team_gold(cur, team_name, 30)
    sql.update_player_hp(cur, player_name, -10)
    sql.give_team_item(cur, "Fire", "Potion")
    sql.give_team_item(cur,"Psychic","Amulet-Coin")
    sql.update_player_experience(cur, "Aaron", 100)
    sql.update_player_experience(cur,"Tommy",-1)
    sql.update_player_experience(cur,"Nicole",1000)
    sql.update_player_experience(cur,"Ronald",2000)

    #Printing list of all the tables
    for team_name in cur.execute(sql.find_all_teams_sql).fetchall():
        print("Team name: ", team_name[1], ", Scores: ", sql.get_team_experience(cur,team_name[1]))

    sql.update_player_team(cur,"Ronald","Rock")

    for team_name in cur.execute(sql.find_all_teams_sql).fetchall():
        print("Team name: ", team_name[1], ", Scores: ", sql.get_team_experience(cur,team_name[1]))

    
    sql.drop_tables()
