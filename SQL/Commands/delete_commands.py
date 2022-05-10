DELETE_ITEM_FROM_TEAMS = """
    DELETE from teams_items
    WHERE rowid=(
        SELECT MIN(rowid)
        from teams_items
        WHERE team_id=
        (
            SELECT team_id
            FROM teams
            WHERE name=?
        )
        AND item_id=
        (
            SELECT item_id
            FROM items
            WHERE name=?
        )
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