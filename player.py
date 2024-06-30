from database import link_connection


class Player:
    default_bucks = 0
    con, cur = link_connection()

    def __init__(self, *, id: str = None):
        if id is None:
            raise TypeError('Id is None')

        self.id = id
        self.bucks = self.get_bucks()
        print(self.bucks)

    def get_bucks(self) -> int:
        res = Player.cur.execute("""
            SELECT bucks FROM players WHERE player_id = ? LIMIT 1
        """, (self.id,))
        fetch = res.fetchone()
        if fetch is None:
            Player.cur.execute("INSERT INTO players (player_id, bucks) VALUES (?, ?)", (self.id, 0))
            Player.con.commit()
            return 0

        bucks = fetch[0]
        return bucks


def main() -> None:
    Player(id='0')


if __name__ == '__main__':
    main()
