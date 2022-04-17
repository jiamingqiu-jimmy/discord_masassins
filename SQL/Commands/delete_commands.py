DELETE_ITEM_FROM_TEAMS = """
    DELETE from teams_items
    WHERE team_id=
    (
        SELECT team_id
        FROM teams
        WHERE name=?
        LIMIT 1
    )
    AND item_id=
    (
        SELECT item_id
        FROM items
        WHERE name=?
        LIMIT 1
    )
"""

DELETE_PLAYER = """
    DELETE from players
    WHERE name=?
"""

DELETE_ITEMS_FROM_PLAYER = """
    DELETE from players_items
    WHERE player_id =
    (
        SELECT player_id
        FROM players
        WHERE name=?
    )
"""