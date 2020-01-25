import sqlite3
import settings

def view_players(cur, team_name):
    view_players = """
        SELECT name, health, experience
        FROM players
        WHERE team_id=
        (SELECT team_id FROM teams WHERE name=?)
        ORDER BY experience, health
    """
    return cur.execute(view_players, [team_name]).fetchall()

def view_teams(cur, team_name):
    view_teams = """
        SELECT gold, experience
        FROM teams
        WHERE name=?
    """
    return cur.execute(view_teams, [team_name]).fetchone()

def view_team_items(cur, team_name):
    view_team_items = """
        SELECT name
        FROM items
        WHERE item_id IN (
            SELECT item_id
            FROM teams_items
            WHERE team_id=(
                SELECT team_id
                FROM teams
                WHERE name=?
            )
        )
    """
    return cur.execute(view_team_items, [team_name]).fetchall()

def view_player_items(cur, player_name):
    view_player_items = """
        SELECT name
        FROM items
        WHERE item_id = (
            SELECT item_id
            FROM players_items
            WHERE player_id = (
                SELECT player_id
                FROM players
                WHERE name=?
            )
        )
    """
    return cur.execute(view_player_items, [player_name]).fetchall()

def find_team_item(cur, team_name, item_name):
    find_team_item = """
        SELECT *
        FROM teams_items
        WHERE team_id= 
        (SELECT team_id FROM teams WHERE name=?)
        AND item_id=
        (SELECT item_id FROM items WHERE name=?)
    """
    cur.execute(find_team_item, (team_name, item_name))
    r = cur.fetchone()
    return r

def find_player_item(cur, player_name, item_name):
    find_player_item = """
        SELECT *
        FROM players_items
        WHERE player_id=
        (SELECT player_id FROM players WHERE name=?)
        AND item_id=
        (SELECT item_id FROM items WHERE name=?)
    """
    cur.execute(find_player_item, (player_name, item_name))
    r = cur.fetchone()
    return r

def delete_item_from_team(cur, team_name, item_name):
    delete_item_from_team = """
    DELETE from teams_items
    WHERE team_id=
    (
        SELECT team_id
        FROM teams
        WHERE name=?
        LIMIT 1
    )
    """
    cur.execute(delete_item_from_team, [team_name])
    cur.connection.commit()

def team_name_from_team_id(cur, team_id):
    team_name_from_team_id = """
        SELECT name
        FROM teams
        WHERE team_id=?
    """
    cur.execute(team_name_from_team_id, [team_id])
    r = cur.fetchone()
    return r[0]

def find_team_name_from_player(cur, player_name):
    find_team_name_from_player = """
    SELECT name FROM teams where team_id=(
        SELECT team_id FROM players where name=?
    )
    """
    cur.execute(find_team_name_from_player, [player_name])
    r = cur.fetchone()
    return r[0]

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

    drop_table_players_items = """
    DROP TABLE IF EXISTS players_items
    """
    cur.execute(drop_table_players_items)

    cur.connection.commit()

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
        experience INTEGER NOT NULL,
        team_id INTEGER NOT NULL,
        discord_id INTEGER UNIQUE,
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
            REFERENCES items (item_id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION
    )
    """
    cur.execute(create_players_items_table)

    create_teams_items_table = """
    CREATE TABLE teams_items (
        team_id INTEGER,
        item_id INTEGER,
        PRIMARY KEY (team_id, item_id),
        FOREIGN KEY (team_id)
            REFERENCES teams (team_id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION,
        FOREIGN KEY (item_id)
            REFERENCES items(item_id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION
    )"""
    cur.execute(create_teams_items_table)
    cur.connection.commit()

def populate_items_table( cur, item_dict ):
    populate_items_table = """
    INSERT INTO items (name, description) VALUES (?,?)
    """
    for item in item_dict.items():
        print("Item : ", item)
        cur.execute(populate_items_table,item)
    cur.connection.commit()
    
def populate_teams_table( cur, team_list ):
    populate_teams_table = """
    INSERT INTO teams (name, experience, gold) VALUES (?, ?, ?)
    """
    for team_name in team_list:
        print("INSERT Team Name :", team_name)
        cur.execute(populate_teams_table, (team_name, settings.team_starting_experience, settings.team_starting_gold))
    cur.connection.commit()

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
    INSERT INTO players (name, health, experience, team_id) VALUES (?,?,?,?)
    """
    valid_team_code = valid_team_check(cur, team_name)
    if valid_team_code != 0:
        return -1
    team_id = find_team_id(cur, team_name)
    new_player = (player_name, settings.new_player_starting_health, settings.new_player_starting_experience, team_id)
    cur.execute(populate_players_table, new_player)
    cur.connection.commit()
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
   cur.connection.commit()

#Update Team Experience
def update_team_experience(cur, team_name, experience_increase_decrease_amount):
    update_team_experience = """
    UPDATE teams
    SET experience = experience+?
    WHERE name=?
    """
    cur.execute(update_team_experience, (experience_increase_decrease_amount, team_name))
    cur.connection.commit()

#Update Player Experience
def update_player_experience(cur, player_name, experience_increase_decrease_amount):
    update_player_experience = """
    UPDATE players
    SET experience = experience+?
    WHERE name=?
    """
    cur.execute(update_player_experience, (experience_increase_decrease_amount, player_name))
    cur.connection.commit()

#Give HP
def update_player_hp(cur, player_name, hp_increase_decrease_amount):
    update_player_hp = """
    UPDATE players
    SET health = health+?
    WHERE name=?
    """
    cur.execute(update_player_hp, (hp_increase_decrease_amount, player_name))
    cur.connection.commit()

#Get player HP
def get_player_hp(cur, player_name):
    get_player_hp = """
    SELECT health
    FROM players
    WHERE name=?
    """
    cur.execute(get_player_hp, [player_name])
    r = cur.fetchone()
    return r[0]

#Get team gold amount
def get_team_gold(cur, team_name):
    get_team_gold = """
    SELECT gold
    FROM teams
    WHERE name=?
    """
    cur.execute(get_team_gold, [team_name])
    r = cur.fetchone()
    return r[0]

#Give Item to Team 
def give_team_item(cur, team_name, item_name):
    give_team_item = """
    INSERT INTO teams_items (team_id, item_id) 
    VALUES (?,?)
    """
    team_id = find_team_id(cur, team_name)
    item_id = find_item_id(cur, item_name)
    print("Team : ", team_id, " Item_ID : ", item_id)
    cur.execute(give_team_item, (team_id, item_id))
    cur.connection.commit()

#Give Item to Player
def give_player_item(cur, player_name, item_name):
    give_player_item = """
    INSERT INTO players_items (player_id, item_id)
    VALUES (?,?)
    """
    player_id = find_player_id(cur, player_name)
    item_id = find_item_id(cur, item_name)
    print("Player : ", player_id, " Item_ID : ", item_id)
    cur.execute(give_player_item, (player_id, item_id))
    cur.connection.commit()

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