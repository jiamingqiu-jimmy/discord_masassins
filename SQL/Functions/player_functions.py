import SQL.Commands.create_commands as create_commands
import SQL.Commands.select_commands as select_commands
import SQL.Commands.delete_commands as delete_commands
import SQL.Commands.drop_commands as drop_commands
import SQL.Commands.insert_commands as insert_commands
import SQL.Commands.update_commands as update_commands

def get_players_from_team(cur, team_name):
    return cur.execute(select_commands.SELECT_PLAYERS, [team_name]).fetchall()

def get_player_team_name(cur, player_name):
    cur.execute(select_commands.SELECT_TEAM_NAME_FROM_PLAYER_NAME, [player_name])
    r = cur.fetchone()
    return r[0]

#Get player HP
def get_player_hp(cur, player_name):
    cur.execute(select_commands.SELECT_PLAYER_HEALTH, [player_name])
    r = cur.fetchone()
    return r[0]

def get_player_item(cur, player_name, item_name):
    cur.execute(select_commands.SELECT_PLAYER_ITEMS, (player_name, item_name))
    r = cur.fetchone()
    return r

def get_player_items(cur, player_name):
    return cur.execute(select_commands.SELECT_PLAYER_ITEMS, [player_name]).fetchall()

def delete_player(cur, player_name):
    cur.execute(delete_commands.DELETE_PLAYER, [player_name])
    cur.connection.commit()

def delete_player_items(cur, player_name):
    cur.execute(delete_commands.DELETE_ITEMS_FROM_PLAYER, [player_name])
    cur.connection.commit()
    
def get_player_id_from_player_name(cur, player_name):
    cur.execute(select_commands.SELECT_PLAYER_ID_FROM_PLAYER_NAME, [player_name])
    r = cur.fetchone()
    return r[0]

#Update Player Experience
def update_player_experience(cur, player_name, experience_increase_decrease_amount):
    cur.execute(update_commands.UPDATE_PLAYER_EXPERIENCE, (experience_increase_decrease_amount, player_name))
    cur.connection.commit()

#Give HP
def update_player_hp(cur, player_name, hp_increase_decrease_amount):
    cur.execute(update_commands.UPDATE_PLAYER_HEALTH, (hp_increase_decrease_amount, player_name))
    cur.connection.commit()