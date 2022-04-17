import sqlite3
import settings

import SQL.Commands.create_commands as create_commands
import SQL.Commands.select_commands as select_commands
import SQL.Commands.delete_commands as delete_commands
import SQL.Commands.drop_commands as drop_commands
import SQL.Commands.insert_commands as insert_commands
import SQL.Commands.update_commands as update_commands

from SQL.Functions.player_functions import * 
from SQL.Functions.team_functions import *
from SQL.Functions.item_functions import *

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
        cur.execute(select_commands.SELECT_PLAYER_WITH_NAME, [player_name])
        rows = cur.fetchall()
        if len(rows) == 0:
            return -2
    except sqlite3.Error:
        return -1
    return 0

def valid_item_check( cur, item_name ):
    try:
        cur.execute(select_commands.SELECT_ALL_PLAYERS_WITH_NAME, [item_name])
        rows = cur.fetchall()
        if len(rows) == 0:
            return -2
    except sqlite3.Error:
        return -1
    return 0

def insert_player(cur, player_name, team_name ):
    valid_team_code = valid_team_check(cur, team_name)
    if valid_team_code != 0:
        return -1
    team_id = get_team_id_from_team_name(cur, team_name)
    new_player = 0
    if team_name == settings.team_name_alumni or team_name == settings.team_name_team_rocket:
        new_player = (player_name, settings.alumni_player_starting_health, settings.alumni_player_starting_experience, team_id)
    else:
        new_player = (player_name, settings.new_player_starting_health, settings.new_player_starting_experience, team_id)
    cur.execute(insert_commands.INSERT_PLAYER, new_player)
    cur.connection.commit()
    return 0

#Give Item to Team 
def give_team_item(cur, team_name, item_name):
    team_id = get_team_id_from_team_name(cur, team_name)
    item_id = get_item_id_from_item_name(cur, item_name)
    cur.execute(insert_commands.INSERT_TEAM_ITEM, (team_id, item_id))
    cur.connection.commit()

#Give Item to Player
def give_player_item(cur, player_name, item_name): 
    player_id = get_player_id_from_player_name(cur, player_name)
    item_id = get_item_id_from_item_name(cur, item_name)
    cur.execute(insert_commands.INSERT_PLAYER_ITEM, (player_id, item_id))
    cur.connection.commit()

#Returns total of team's player's experience
def get_team_experience(cur, team_name):
    exp = [i[2] for i in get_players_from_team(cur, team_name)]
    return sum(exp)

def update_player_team(cur,player_name,team_name):
    if valid_team_check(cur,team_name)!=0:
        return -1
    if valid_player_check(cur,player_name)!=0:
        return -2
    team_id = get_team_id_from_team_name(cur, team_name)
    cur.execute(update_commands.UPDATE_PLAYER_TEAM,(team_id,player_name))
    cur.connection.commit()