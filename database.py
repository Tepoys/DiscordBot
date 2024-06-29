import sqlite3


def load_user_data() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    # connect to DB
    con_local: sqlite3.Connection = sqlite3.connect("database.sqlite")
    # create cursor for modification
    cur_local: sqlite3.Cursor = con_local.cursor()

    # create table for value storage
    # cur_local.execute("CREATE TABLE IF NOT EXISTS users(id, money, ")

    return con_local, cur_local


con, cur = load_user_data()


