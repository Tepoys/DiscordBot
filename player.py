from database import link_connection
from shop import Shop


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

    def change_bucks(self, change_amount: int) -> None:
        Player.cur.execute("UPDATE players SET bucks = bucks + ? WHERE player_id = ?",
                           [(change_amount,), (self.id,)])

        Player.con.commit()

    def buy(self, item_name: str, store_id: str, shops: dict[str, Shop]) -> bool:
        """
        Buys item_name from store_id
        :param shops: list of shops to find item in
        :param item_name: Name of the item to buy
        :param store_id: The store of where the item is
        :return: true if the item was successfully bought and false otherwise
        """
        store = shops.get(store_id)
        if store is None:
            print(f'Store {store_id} does not exist')
            return False

        item_cost: int = store.cost(item_name)

        if item_cost is None:
            print(f'Item {item_name} does not exist in store {store_id}')
            return False

        self.change_bucks(item_cost*-1)

        return True

def cleanup_player() -> None:
    Player.con.close()

def main() -> None:
    Player(id='0')


if __name__ == '__main__':
    main()
