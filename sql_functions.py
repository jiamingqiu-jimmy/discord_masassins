import sqlite3
import settings

import SQL.create_commands as create_commands
import SQL.select_commands as select_commands
import SQL.delete_commands as delete_commands
import SQL.drop_commands as drop_commands
import SQL.insert_commands as insert_commands
import SQL.update_commands as update_commands

def view_players(cur, team_name):
    return cur.execute(select_commands.SELECT_PLAYERS, [team_name]).fetchall()

def view_teams(cur, team_name):
    return cur.execute(select_commands.SELECT_TEAMS, [team_name]).fetchone()

def view_team_items(cur, team_name):
    return cur.execute(select_commands.SELECT_TEAM_ITEMS, [team_name]).fetchall()

def view_team_item_count(cur, team_name, item_name):
    return cur.execute(select_commands.SELECT_TEAM_ITEM_COUNT, (team_name, item_name)).fetchone()

def view_player_items(cur, player_name):
    return cur.execute(select_commands.SELECT_PLAYER_ITEMS, [player_name]).fetchall()

def find_team_item(cur, team_name, item_name):
    cur.execute(select_commands.SELECT_TEAM_ITEMS, (team_name, item_name))
    r = cur.fetchone()
    return r

def find_player_item(cur, player_name, item_name):
    cur.execute(select_commands.SELECT_PLAYER_ITEMS, (player_name, item_name))
    r = cur.fetchone()
    return r

def delete_item_from_team(cur, team_name, item_name):
    cur.execute(delete_commands.DELETE_ITEM_FROM_TEAMS, (team_name, item_name))
    cur.connection.commit()

def delete_player(cur, player_name):
    cur.execute(delete_commands.DELETE_PLAYER, [player_name])
    cur.connection.commit()

def delete_items_from_player(cur, player_name):
    cur.execute(delete_commands.DELETE_ITEMS_FROM_PLAYER, [player_name])
    cur.connection.commit()

def team_name_from_team_id(cur, team_id):
    cur.execute(select_commands.SELECT_TEAM_NAME_FROM_TEAM_ID, [team_id])
    r = cur.fetchone()
    return r[0]

def find_team_name_from_player(cur, player_name):
    cur.execute(select_commands.SELECT_TEAM_NAME_FROM_PLAYER_NAME, [player_name])
    r = cur.fetchone()
    return r[0]

def find_team_id(cur, team_name):
    cur.execute(select_commands.SELECT_TEAM_ID_FROM_TEAM_NAME, [team_name])
    r = cur.fetchone()
    return r[0]

def find_player_id(cur, player_name):
    cur.execute(select_commands.SELECT_PLAYER_ID_FROM_PLAYER_NAME, [player_name])
    r = cur.fetchone()
    return r[0]

def find_item_id(cur, item_name):
    cur.execute(select_commands.SELECT_ITEM_ID_FROM_ITEM_NAME, [item_name])
    r = cur.fetchone()
    return r[0]

def drop_tables(cur):
    cur.execute(drop_commands.DROP_TABLE_PLAYERS)
    cur.execute(drop_commands.DROP_TABLE_TEAMS)
    cur.execute(drop_commands.DROP_TABLE_ITEMS)
    cur.execute(drop_commands.DROP_TABLE_TEAMS_ITEMS)
    cur.execute(drop_commands.DROP_TABLE_PLAYERS_ITEMS)
    cur.connection.commit()

def create_tables(cur):
    cur.execute(create_commands.CREATE_TEAM_TABLES)
    cur.execute(create_commands.CREATE_PLAYERS_TABLE)
    cur.execute(create_commands.CREATE_ITEMS_TABLE)
    cur.execute(create_commands.CREATE_PLAYERS_ITEMS_TABLE)
    cur.execute(create_commands.CREATE_TEAMS_ITEMS_TABLE)
    cur.connection.commit()

def populate_items_table( cur, item_dict ):
    for item in item_dict.items():
        cur.execute(insert_commands.INSERT_ITEM,item)
    cur.connection.commit()
    
def populate_teams_table( cur, team_list ):
    for team_name in team_list:
        cur.execute(insert_commands.INSERT_TEAM, (team_name, settings.team_starting_experience, settings.team_starting_gold))
    cur.connection.commit()

def valid_team_check( cur, team_name ):
    try:
        cur.execute(select_commands.SELECT_ALL_FROM_TEAMS_WITH_TEAM_NAME, [team_name])
        rows = cur.fetchall()
        if len(rows) == 0:
            return -2
    except sqlite3.Error:
        return -1
    return 0

def valid_player_check( cur, player_name ):
    try:
        cur.execute(select_commands.SELECT_PLAYER_ITEMS, [player_name])
        rows = cur.fetchall()
        if len(rows) == 0:
            return -2
    except sqlite3.Error:
        return -1
    return 0

def valid_item_check( cur, item_name ):
    try:
        cur.execute(select_commands.SELECT_ALL_ITEMS_WITH_NAME, [item_name])
        rows = cur.fetchall()
        if len(rows) == 0:
            return -2
    except sqlite3.Error:
        return -1
    return 0

def populate_players_table( cur, player_name, team_name ):
    valid_team_code = valid_team_check(cur, team_name)
    if valid_team_code != 0:
        return -1
    team_id = find_team_id(cur, team_name)
    new_player = 0
    if team_name == settings.team_name_alumni or team_name == settings.team_name_team_rocket:
        new_player = (player_name, settings.alumni_player_starting_health, settings.alumni_player_starting_experience, team_id)
    else:
        new_player = (player_name, settings.new_player_starting_health, settings.new_player_starting_experience, team_id)
    cur.execute(insert_commands.INSERT_PLAYER, new_player)
    cur.connection.commit()
    return 0

#Give Gold
def update_team_gold(cur, team_name, gold_increase_decrease_amount):
   cur.execute(update_commands.UPDATE_TEAM_GOLD, (gold_increase_decrease_amount, team_name))
   cur.connection.commit()

#Update Player Experience
def update_player_experience(cur, player_name, experience_increase_decrease_amount):
    cur.execute(update_commands.UPDATE_PLAYER_EXPERIENCE, (experience_increase_decrease_amount, player_name))
    cur.connection.commit()

#Give HP
def update_player_hp(cur, player_name, hp_increase_decrease_amount):
    cur.execute(update_commands.UPDATE_PLAYER_HEALTH, (hp_increase_decrease_amount, player_name))
    cur.connection.commit()

#Get player HP
def get_player_hp(cur, player_name):
    cur.execute(select_commands.SELECT_PLAYER_HEALTH, [player_name])
    r = cur.fetchone()
    return r[0]

#Get team gold amount
def get_team_gold(cur, team_name):
    cur.execute(select_commands.SELECT_TEAM_GOLD, [team_name])
    r = cur.fetchone()
    return r[0]

#Give Item to Team 
def give_team_item(cur, team_name, item_name):
    team_id = find_team_id(cur, team_name)
    item_id = find_item_id(cur, item_name)
    cur.execute(insert_commands.INSERT_TEAM_ITEM, (team_id, item_id))
    cur.connection.commit()

#Give Item to Player
def give_player_item(cur, player_name, item_name): 
    player_id = find_player_id(cur, player_name)
    item_id = find_item_id(cur, item_name)
    cur.execute(insert_commands.INSERT_PLAYER_ITEM, (player_id, item_id))
    cur.connection.commit()

#Returns total of team's player's experience
def get_team_experience(cur, team_name):
    exp = [i[2] for i in view_players(cur, team_name)]
    return sum(exp)

def update_player_team(cur,player_name,team_name):
    if valid_team_check(cur,team_name)!=0:
        return -1
    if valid_player_check(cur,player_name)!=0:
        return -2
    team_id = find_team_id(cur, team_name)
    cur.execute(update_commands.UPDATE_PLAYER_TEAM,(team_id,player_name))
    cur.connection.commit()

def view_teams_list(cur, team_list):
    cur.execute(select_commands.SELECT_ALL_TEAMS)
    rows = cur.fetchall()
    for row in rows:
        team_list.append(row)
