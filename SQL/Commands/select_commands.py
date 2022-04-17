SELECT_PLAYERS = """
    SELECT name, health, experience
    FROM players
    WHERE team_id=
    (SELECT team_id FROM teams WHERE name=?)
    ORDER BY experience DESC, health DESC
"""

SELECT_ALL_PLAYERS_WITH_NAME = """
    SELECT * FROM players WHERE name=?
"""

SELECT_PLAYER_ITEMS = """
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

SELECT_PLAYER_HEALTH = """
    SELECT health
    FROM players
    WHERE name=?
"""
    
SELECT_PLAYER_ID_FROM_PLAYER_NAME = """
    SELECT player_id
    FROM players
    WHERE name=?
"""

SELECT_PLAYER_ITEMS = """
    SELECT *
    FROM players_items
    WHERE player_id=
    (SELECT player_id FROM players WHERE name=?)
    AND item_id=
    (SELECT item_id FROM items WHERE name=?)
"""

SELECT_ALL_TEAMS = """ SELECT * FROM teams """

SELECT_ALL_FROM_TEAMS_WITH_TEAM_NAME = """
    SELECT * FROM teams WHERE name=?
"""

SELECT_TEAM_ITEMS = """
    SELECT *
    FROM teams_items
    WHERE team_id= 
    (SELECT team_id FROM teams WHERE name=?)
    AND item_id=
    (SELECT item_id FROM items WHERE name=?)
"""

SELECT_TEAM_GOLD = """
    SELECT gold
    FROM teams
    WHERE name=?
"""

SELECT_TEAM_NAME_FROM_TEAM_ID = """
    SELECT name
    FROM teams
    WHERE team_id=?
"""

SELECT_TEAM_ID_FROM_TEAM_NAME = """
    SELECT team_id FROM teams WHERE name=? 
"""

SELECT_TEAM_NAME_FROM_PLAYER_NAME = """
    SELECT name FROM teams where team_id=(
        SELECT team_id FROM players where name=?
    )
"""

SELECT_TEAMS = """
    SELECT gold, experience
    FROM teams
    WHERE name=?
"""

SELECT_TEAM_ITEMS = """
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

SELECT_TEAM_ITEM_COUNT = """
    SELECT COUNT(*)
    FROM (
        SELECT item_id
        FROM teams_items
        WHERE team_id = (
            SELECT team_id
            FROM teams
            WHERE name=?
        )
        AND item_id = (
            SELECT item_id
            FROM items
            WHERE name=?
        )
    )
"""

SELECT_ALL_ITEMS_WITH_NAME = """
    SELECT * FROM items WHERE name=?
"""

SELECT_ITEM_ID_FROM_ITEM_NAME = """
    SELECT item_id FROM items where name=?
"""
