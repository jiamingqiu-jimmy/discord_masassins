INSERT_ITEM = """
    INSERT INTO items (name, description) VALUES (?,?)
"""

INSERT_TEAM = """
    INSERT INTO teams (name, experience, gold) VALUES (?, ?, ?)
"""

INSERT_PLAYER = """
    INSERT INTO players (name, health, experience, team_id) VALUES (?,?,?,?)
"""

