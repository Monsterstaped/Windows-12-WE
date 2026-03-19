import sqlite3
def create_tables():
    con = sqlite3.connect("settings.db")
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY,
        brightness INTEGER,
        hide_icons INTEGER,
        wallpaper INTEGER
    )
    """)
    cur.execute("SELECT COUNT(*) FROM settings")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO settings (brightness, hide_icons, wallpaper) VALUES (100, 0, 0)"
        )
    con.commit()
    con.close()
def load_settings():
    con = sqlite3.connect("settings.db")
    cur = con.cursor()
    cur.execute("SELECT brightness, hide_icons, wallpaper FROM settings WHERE id=1")
    data = cur.fetchone()
    con.close()
    return data
def save_settings(brightness=None, hide_icons=None, wallpaper=None):
    con = sqlite3.connect("settings.db")
    cur = con.cursor()
    if brightness is not None:
        cur.execute("UPDATE settings SET brightness=? WHERE id=1", (brightness,))
    if hide_icons is not None:
        cur.execute("UPDATE settings SET hide_icons=? WHERE id=1", (hide_icons,))
    if wallpaper is not None:
        cur.execute("UPDATE settings SET wallpaper=? WHERE id=1", (wallpaper,))
    con.commit()
    con.close()