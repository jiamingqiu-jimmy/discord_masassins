CREATE_TEAM_TABLES="""
    CREATE TABLE teams (
        team_id INTEGER PRIMARY KEY,
        name text NOT NULL UNIQUE,
        experience INTEGER NOT NULL,
        gold INTEGER NOT NULL
    )
    """

CREATE_PLAYERS_TABLE="""
    CREATE TABLE players (
        player_id INTEGER PRIMARY KEY,
        name text NOT NULL UNIQUE,
        health INTEGER NOT NULL,
        experience INTEGER NOT NULL,
        team_id INTEGER NOT NULL,
        discord_id INTEGER UNIQUE,
        FOREIGN KEY (team_id)
            REFERENCES teams (team_id)
    )
    """

CREATE_PLAYERS_ITEMS_TABLE="""
    CREATE TABLE players_items (
        player_item_id PRIMARY KEY,
        player_id INTEGER,
        item_id INTEGER,
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

CREATE_TEAMS_ITEMS_TABLE="""
    CREATE TABLE teams_items (
        team_item_id PRIMARY KEY,
        team_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        FOREIGN KEY (team_id)
            REFERENCES teams (team_id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION,
        FOREIGN KEY (item_id)
            REFERENCES items(item_id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION
    )"""
