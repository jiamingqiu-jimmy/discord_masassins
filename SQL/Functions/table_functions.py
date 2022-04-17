import SQL.Commands.create_commands as create_commands
import SQL.Commands.drop_commands as drop_commands

def create_teams_table(cur):
    cur.execute(create_commands.CREATE_TEAM_TABLES)
    cur.connection.commit()

def create_players_table(cur):
    cur.execute(create_commands.CREATE_PLAYERS_TABLE)
    cur.connection.commit()

def create_items_table(cur):
    cur.execute(create_commands.CREATE_ITEMS_TABLE)
    cur.connection.commit()

def create_players_items_table(cur):
    cur.execute(create_commands.CREATE_PLAYERS_ITEMS_TABLE)
    cur.connection.commit()

def create_teams_items_table(cur):
    cur.execute(create_commands.CREATE_TEAMS_ITEMS_TABLE)
    cur.connection.commit()

def drop_players_table(cur):
    cur.execute(drop_commands.DROP_TABLE_PLAYERS)
    cur.connection.commit()
    
def drop_teams_table(cur):
    cur.execute(drop_commands.DROP_TABLE_TEAMS)
    cur.connection.commit()

def drop_items_table(cur):
    cur.execute(drop_commands.DROP_TABLE_ITEMS)
    cur.connection.commit()

def drop_teams_items_table(cur):
    cur.execute(drop_commands.DROP_TABLE_TEAMS_ITEMS)
    cur.connection.commit()

def drop_players_items_table(cur):
    cur.execute(drop_commands.DROP_TABLE_PLAYERS_ITEMS)
    cur.connection.commit()