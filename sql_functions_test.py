import sqlite3
import settings
import sql_functions as sql
import importlib
import pytest
import random

def test_simple_player_interaction():
    importlib.reload(sql)
    conn = sqlite3.connect('SQLTEST.db')
    cur = conn.cursor()
    sql.drop_tables(cur)
    sql.create_tables(cur)
    sql.insert_items( cur, settings.item_dict )
    sql.insert_teams( cur, settings.team_list )
    for player_name,team_name in settings.player_team_dict.items():
        assert(sql.valid_team_check(cur, team_name) == 0)
        sql.insert_player(cur, player_name, team_name)
    
    player_name = random.choice(list(settings.player_team_dict))
    player_team_name = settings.player_team_dict[player_name]
    
    sql.update_team_gold(cur, team_name, 30)
    assert sql.get_team_gold(cur, team_name) == 30
    
    previous_hp = sql.get_player_hp(cur,player_name)
    sql.update_player_hp(cur, player_name, -10)
    assert sql.get_player_hp(cur, player_name) == previous_hp-10
    
    sql.update_player_hp(cur, player_name, 10)
    assert sql.get_player_hp(cur, player_name) == previous_hp
    
    sql.give_team_item(cur, "Fire", "Potion")
    print(sql.get_team_item_count(cur, "Fire", "Potion"))
    assert sql.get_team_item_count(cur, "Fire", "Potion") == 1
    assert sql.get_team_item_count(cur, "Fire", "Revive") == 0
    
    sql.update_player_experience(cur, player_name, 100)
    assert sql.get_player_experience(cur, player_name) == 100
    assert sql.get_team_experience(cur, player_team_name) == 100
    
    sql.update_team_gold(cur, player_team_name, 40)
    assert sql.get_team_gold(cur, player_team_name) == 40

    sql.update_team_gold(cur, player_team_name, -20)
    assert sql.get_team_gold(cur, player_team_name) == 20
    
    print(f'player: {player_name} with {sql.get_player_experience(cur, player_name)} in {team_name}')
    print(f'Team experience {sql.get_team_experience(cur,player_team_name)}')
    print("--------------")
    sql.update_player_team(cur,"Ronald","Rock")
    assert sql.get_player_team_name(cur, "Ronald") == "Rock"