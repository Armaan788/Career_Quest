import sqlite3


def get_db():

    conn = sqlite3.connect("career_quest.db")

    conn.row_factory = sqlite3.Row

    return conn


def initialize_database():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS players (

            name TEXT PRIMARY KEY,

            xp INTEGER DEFAULT 0,

            careers_completed INTEGER DEFAULT 0,

            current_streak INTEGER DEFAULT 0,

            best_streak INTEGER DEFAULT 0,

            last_active TEXT
        )
    """)

    columns = conn.execute(
        "PRAGMA table_info(players)"
    ).fetchall()

    column_names = [column["name"] for column in columns]

    if "current_streak" not in column_names:

        conn.execute(
            "ALTER TABLE players ADD COLUMN current_streak INTEGER DEFAULT 0"
        )

    if "best_streak" not in column_names:

        conn.execute(
            "ALTER TABLE players ADD COLUMN best_streak INTEGER DEFAULT 0"
        )

    if "last_active" not in column_names:

        conn.execute(
            "ALTER TABLE players ADD COLUMN last_active TEXT"
        )

    conn.execute("""
        CREATE TABLE IF NOT EXISTS site_stats (

            id INTEGER PRIMARY KEY,

            visits INTEGER DEFAULT 0
        )
    """)

    conn.execute("""
        INSERT OR IGNORE INTO site_stats (id, visits)
        VALUES (1, 0)
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS achievements (

            player_name TEXT,

            title TEXT,

            PRIMARY KEY (player_name, title),

            FOREIGN KEY (player_name) REFERENCES players(name)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS career_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            player_name TEXT,

            career TEXT,

            score INTEGER,

            completed_at TEXT,

            FOREIGN KEY (player_name) REFERENCES players(name)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS saved_careers (

            player_name TEXT,

            career TEXT,

            PRIMARY KEY (player_name, career),

            FOREIGN KEY (player_name) REFERENCES players(name)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS match_results (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            player_name TEXT,

            top_career TEXT,

            second_career TEXT,

            third_career TEXT,

            completed_at TEXT,

            FOREIGN KEY (player_name) REFERENCES players(name)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_challenges (

            player_name TEXT,

            challenge_date TEXT,

            career TEXT,

            completed INTEGER DEFAULT 0,

            PRIMARY KEY (player_name, challenge_date),

            FOREIGN KEY (player_name) REFERENCES players(name)
        )
    """)

    conn.commit()

    conn.close()


if __name__ == "__main__":

    initialize_database()

    print("Database updated successfully")