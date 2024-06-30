import sqlite3


def link_connection() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    # connect to DB
    con_local: sqlite3.Connection = sqlite3.connect("database.sqlite")
    # create cursor for modification
    cur_local: sqlite3.Cursor = con_local.cursor()
    # return variables in tuple
    return con_local, cur_local


def main() -> None:
    con, cur = link_connection()


if __name__ == "__main__":
    main()
