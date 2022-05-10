UPDATE_TEAM_GOLD = """
   UPDATE teams
   SET gold = gold+?
   WHERE name=?
"""

UPDATE_PLAYER_EXPERIENCE = """
    UPDATE players
    SET experience = experience+?
    WHERE name=?
"""

UPDATE_PLAYER_HEALTH = """
    UPDATE players
    SET health = health+?
    WHERE name=?
"""

UPDATE_PLAYER_TEAM = """
    UPDATE players
    SET team_id = ?
    WHERE name = ?
"""

UPDATE_TEAM_NAME = """
    UPDATE teams
    SET name = ?
    WHERE name = ?
"""