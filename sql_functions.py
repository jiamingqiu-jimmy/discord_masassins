import sqlite3
import settings

def drop_tables(cur):
    drop_table_players = """
    DROP TABLE IF EXISTS players
    """
    cur.execute(drop_table_players)

    drop_table_teams = """
    DROP TABLE IF EXISTS teams
    """
    cur.execute(drop_table_teams)

    drop_table_items = """
    DROP TABLE IF EXISTS items
    """
    cur.execute(drop_table_items)
    
    drop_table_players_items = """
    DROP TABLE IF EXISTS players_items
    """
    cur.execute(drop_table_players_items)

def create_tables(cur):
    create_teams_table = """
    CREATE TABLE teams (
        team_id INTEGER PRIMARY KEY,
        name text NOT NULL UNIQUE
    )"""
    cur.execute(create_teams_table)

    create_items_table = """
    CREATE TABLE items (
        item_id INTEGER PIMARY KEY,
        name text NOT NULL UNIQUE,
        description text NOT NULL
    )"""
    cur.execute(create_items_table)

    create_players_table = """
    CREATE TABLE players (
        player_id INTEGER PRIMARY KEY,
        name text NOT NULL UNIQUE,
        health INTEGER NOT NULL,
        gold INTEGER NOT NULL,
        team_id INTEGER NOT NULL,
        FOREIGN KEY (team_id)
            REFERENCES teams (team_id)
    )"""
    cur.execute(create_players_table)

    create_players_items_table = """
    CREATE TABLE players_items (
        player_id INTEGER,
        item_id INTEGER,
        PRIMARY KEY (player_id, item_id),
        FOREIGN KEY (player_id)
            REFERENCES players (player_id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION,
        FOREIGN KEY (item_id)
            REFERENCES items(item_id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION
    )"""
    cur.execute(create_players_items_table)

def populate_items_table( cur, item_dict ):
    populate_items_table = """
    INSERT INTO items (name, description) VALUES (?,?)
    """
    for item in item_dict.items():
        print("Item : ", item)
        cur.execute(populate_items_table,item)
    
def populate_teams_table( cur, team_list ):
    populate_teams_table = """
    INSERT INTO teams (name) VALUES (?)
    """
    for team_name in team_list:
        print("Team Name :", team_name)
        cur.execute(populate_teams_table, [team_name])

def valid_team_check( cur, team_name ):
    valid_team_check = """
    SELECT * FROM teams WHERE name=?
    """
    try:
        cur.execute(valid_team_check, [team_name])
        rows = cur.fetchall()
        if len(rows) == 0:
            return -2
    except sqlite3.Error:
        return -1
    return 0

def populate_players_table( cur, player_name, team_name ):
    find_team_id = """
    SELECT team_id FROM teams where name=?
    """
    populate_players_table = """
    INSERT INTO players (name, health, gold, team_id) VALUES (?,?,?,?)
    """
    cur.execute(find_team_id, [team_name])
    r = cur.fetchone()
    new_player = (player_name, settings.new_player_starting_health, settings.new_player_starting_gold, r[0])
    cur.execute(populate_players_table, new_player)

def view_teams_list(cur):
    find_all_teams = """
    SELECT * FROM teams
    """
    cur.execute(find_all_teams)
    rows = cur.fetchall()

    for row in rows:
        print("Row : ", row[1])


