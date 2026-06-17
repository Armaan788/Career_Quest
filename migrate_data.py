import json
from pathlib import Path

from database import get_db, initialize_database


def migrate_data():

    initialize_database()
    conn = get_db()

    players_file = Path("players.json")
    stats_file = Path("stats.json")

    if players_file.exists():

        players = json.loads(
            players_file.read_text(encoding="utf-8")
        )

        for name, data in players.items():

            conn.execute(
                """
                INSERT INTO players
                    (name, xp, careers_completed)
                VALUES (?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    xp = MAX(xp, excluded.xp),
                    careers_completed = MAX(
                        careers_completed,
                        excluded.careers_completed
                    )
                """,
                (
                    name,
                    data.get("xp", 0),
                    data.get("careers_completed", 0)
                )
            )

            for achievement in data.get("achievements", []):

                conn.execute(
                    """
                    INSERT OR IGNORE INTO achievements
                        (player_name, title)
                    VALUES (?, ?)
                    """,
                    (name, achievement)
                )

    if stats_file.exists():

        stats = json.loads(
            stats_file.read_text(encoding="utf-8")
        )

        conn.execute(
            """
            UPDATE site_stats
            SET visits = MAX(visits, ?)
            WHERE id = 1
            """,
            (stats.get("visits", 0),)
        )

    conn.commit()
    conn.close()

    print("Old data migrated successfully!")


if __name__ == "__main__":

    migrate_data()