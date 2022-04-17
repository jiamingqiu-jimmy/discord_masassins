import settings

import SQL.Commands.create_commands as create_commands
import SQL.Commands.select_commands as select_commands
import SQL.Commands.delete_commands as delete_commands
import SQL.Commands.drop_commands as drop_commands
import SQL.Commands.insert_commands as insert_commands
import SQL.Commands.update_commands as update_commands

def get_teams(cur, team_name):
    return cur.execute(select_commands.SELECT_TEAMS, [team_name]).fetchone()

#Get team gold amount
def get_team_gold(cur, team_name):
    cur.execute(select_commands.SELECT_TEAM_GOLD, [team_name])
    r = cur.fetchone()
    return r[0]

def view_teams_list(cur, team_list):
    cur.execute(select_commands.SELECT_ALL_TEAMS)
    rows = cur.fetchall()
    for row in rows:
        team_list.append(row)

def get_team_name_from_team_id(cur, team_id):
    cur.execute(select_commands.SELECT_TEAM_NAME_FROM_TEAM_ID, [team_id])
    r = cur.fetchone()
    return r[0]

def get_team_items(cur, team_name):
    return cur.execute(select_commands.SELECT_TEAM_ITEMS, [team_name]).fetchall()

def get_team_item_count(cur, team_name, item_name):
    return cur.execute(select_commands.SELECT_TEAM_ITEM_COUNT, (team_name, item_name)).fetchone()

def get_team_item(cur, team_name, item_name):
    cur.execute(select_commands.SELECT_TEAM_ITEMS, (team_name, item_name))
    r = cur.fetchone()
    return r

def delete_team_item(cur, team_name, item_name):
    cur.execute(delete_commands.DELETE_ITEM_FROM_TEAMS, (team_name, item_name))
    cur.connection.commit()

def get_team_id_from_team_name(cur, team_name):
    cur.execute(select_commands.SELECT_TEAM_ID_FROM_TEAM_NAME, [team_name])
    r = cur.fetchone()
    return r[0]

def insert_teams( cur, team_list ):
    for team_name in team_list:
        cur.execute(insert_commands.INSERT_TEAM, (team_name, settings.team_starting_experience, settings.team_starting_gold))
    cur.connection.commit()
    
#Give Gold
def update_team_gold(cur, team_name, gold_increase_decrease_amount):
   cur.execute(update_commands.UPDATE_TEAM_GOLD, (gold_increase_decrease_amount, team_name))
   cur.connection.commit()