import sqlite3
import settings

def find_team_id(cur, team_name):
    find_team_id = """
    SELECT team_id FROM teams WHERE name=? 
    """
    cur.execute(find_team_id, [team_name])
    r = cur.fetchone()
    return r[0]

def find_player_id(cur, player_name):
    find_player_id = """
    SELECT player_id FROM players WHERE name=?
    """
    cur.execute(find_player_id, [player_name])
    r = cur.fetchone()
    return r[0]

def find_item_id(cur, item_name):
    find_item_id = """
    SELECT item_id FROM items where name=?
    """
    cur.execute(find_item_id, [item_name])
    r = cur.fetchone()
    return r[0]

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
    
    drop_table_teams_items = """
    DROP TABLE IF EXISTS teams_items
    """
    cur.execute(drop_table_teams_items)

def create_tables(cur):
    create_teams_table = """
    CREATE TABLE teams (
        team_id INTEGER PRIMARY KEY,
        name text NOT NULL UNIQUE,
        experience INTEGER NOT NULL,
        gold INTEGER NOT NULL
    )"""
    cur.execute(create_teams_table)

    create_items_table = """
    CREATE TABLE items (
        item_id INTEGER PRIMARY KEY,
        name text NOT NULL UNIQUE,
        description text NOT NULL
    )"""
    cur.execute(create_items_table)

    create_players_table = """
    CREATE TABLE players (
        player_id INTEGER PRIMARY KEY,
        name text NOT NULL UNIQUE,
        health INTEGER NOT NULL,
        team_id INTEGER NOT NULL,
        discord_id INTEGER UNIQUE,
        FOREIGN KEY (team_id)
            REFERENCES teams (team_id)
    )"""
    cur.execute(create_players_table)

    create_teams_items_table = """
    CREATE TABLE teams_items (
        team_id INTEGER,
        item_id INTEGER,
        PRIMARY KEY (team_id, item_id),
        FOREIGN KEY (team_id)
            REFERENCES players (team_id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION,
        FOREIGN KEY (item_id)
            REFERENCES items(item_id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION
    )"""
    cur.execute(create_teams_items_table)

def populate_items_table( cur, item_dict ):
    populate_items_table = """
    INSERT INTO items (name, description) VALUES (?,?)
    """
    for item in item_dict.items():
        print("Item : ", item)
        cur.execute(populate_items_table,item)
    
def populate_teams_table( cur, team_list ):
    populate_teams_table = """
    INSERT INTO teams (name, experience, gold) VALUES (?, ?, ?)
    """
    for team_name in team_list:
        print("INSERT Team Name :", team_name)
        cur.execute(populate_teams_table, (team_name, settings.team_starting_experience, settings.team_starting_gold))

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

def valid_player_check( cur, player_name ):
    valid_player_check = """
    SELECT * FROM players WHERE name=?
    """
    try:
        cur.execute(valid_player_check, [player_name])
        rows = cur.fetchall()
        if len(rows) == 0:
            return -2
    except sqlite3.Error:
        return -1
    return 0

def valid_item_check( cur, item_name ):
    valid_item_check = """
    SELECT * FROM items WHERE name=?
    """
    try:
        cur.execute(valid_item_check, [item_name])
        rows = cur.fetchall()
        if len(rows) == 0:
            return -2
    except sqlite3.Error:
        return -1
    return 0

def populate_players_table( cur, player_name, team_name ):
    populate_players_table = """
    INSERT INTO players (name, health, team_id) VALUES (?,?,?)
    """
    valid_team_code = valid_team_check(cur, team_name)
    if valid_team_code != 0:
        return -1
    team_id = find_team_id(cur, team_name)
    new_player = (player_name, settings.new_player_starting_health, team_id)
    cur.execute(populate_players_table, new_player)
    return 0

#Give Gold
def update_team_gold(cur, team_name, gold_increase_decrease_amount):
   update_team_gold = """
   UPDATE teams
   SET gold = gold+?
   WHERE name=?
   """
   print("Team name : ", [team_name])
   print("Gold Amount : ", [gold_increase_decrease_amount])
   cur.execute(update_team_gold, (gold_increase_decrease_amount, team_name))

#Update Team Experience
def update_team_experience(cur, team_name, experience_increase_decrease_amount):
    update_team_experience = """
    UPDATE teams
    SET experience = experience+?
    WHERE name=?
    """
    cur.execute(update_team_experience, (experience_increase_decrease_amount, team_name))

#Give HP
def update_player_hp(cur, player_name, hp_increase_decrease_amount):
    update_player_hp = """
    UPDATE players
    SET health = health+?
    WHERE name=?
    """
    cur.execute(update_player_hp, (hp_increase_decrease_amount, player_name))

#Give Item
def give_team_item(cur, team_name, item_name):
    give_team_item = """
    INSERT INTO teams_items (team_id, item_id) 
        VALUES (?,?)
    """
    team_id = find_team_id(cur, team_name)
    item_id = find_item_id(cur, item_name)
    print("Team : ", team_id, " Item_ID : ", item_id)
    cur.execute(give_team_item, (team_id, item_id))
    
find_all_teams_sql = """ SELECT * FROM teams """
find_all_players_sql = """ SELECT * FROM players """
find_all_items_sql = """ SELECT * FROM items """
find_all_teams_items_sql = """ SELECT * FROM teams_items """

def view_teams_list(cur, team_list):
    cur.execute(find_all_teams_sql)
    rows = cur.fetchall()
    for row in rows:
        team_list.append(row)

def print_all_list(cur):
    cur.execute(find_all_teams_sql)
    rows = cur.fetchall()
    for row in rows:
        print("Team : ", row)
    
    cur.execute(find_all_players_sql)
    rows = cur.fetchall()
    for row in rows:
        print("Player : ", row)

    cur.execute(find_all_items_sql)
    rows = cur.fetchall()
    for row in rows:
        print("Item : ", row)

    cur.execute(find_all_teams_items_sql)
    rows = cur.fetchall()
    for row in rows:
        print("Player_Item : ", row)