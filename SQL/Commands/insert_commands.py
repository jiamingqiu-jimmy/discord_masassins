INSERT_ITEM = """
    INSERT INTO items (name, description) VALUES (?,?)
"""

INSERT_TEAM = """
    INSERT INTO teams (name, experience, gold) VALUES (?, ?, ?)
"""

INSERT_PLAYER = """
    INSERT INTO players (name, health, experience, team_id) VALUES (?,?,?,?)
"""

INSERT_TEAM_ITEM = """
    INSERT INTO teams_items (team_id, item_id) 
    VALUES (?,?)
"""

INSERT_PLAYER_ITEM = """
    INSERT INTO players_items (player_id, item_id)
    VALUES (?,?)
"""