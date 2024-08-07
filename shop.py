from database import link_connection


def create_tables() -> None:
    con_local, cur_local = link_connection()
    cur_local.execute(
        "CREATE TABLE IF NOT EXISTS menu(store_id TEXT NOT NULL, item_name TEXT PRIMARY KEY, item_cost INT NOT NULL)")
    cur_local.execute("""
        CREATE TABLE IF NOT EXISTS 
            inventory(player_id TEXT NOT NULL, item_name TEXT NOT NULL, count INT NOT NULL, shop_id TEXT NOT NULL)
    """)
    cur_local.execute("CREATE TABLE IF NOT EXISTS players(player_id TEXT PRIMARY KEY, bucks INT NOT NULL)")
    con_local.close()


def create_test_values() -> None:
    inp: str = input("Are you sure you want to create values:")
    if inp.lower() != "y":
        return

    con_local, cur_local = link_connection()
    try:
        cur_local.execute("INSERT INTO menu(store_id, item_name, item_cost) VALUES(?, ?, ?)", ('1', 'item1', 103))
    except Exception as e:
        print(e)


class Shop:
    con, cur = link_connection()

    def __init__(self, id: str) -> None:
        self.id = id
        self.items: dict[str, int] = self.get_items()

    def get_items(self) -> dict[str, int]:
        res = Shop.cur.execute("""
            SELECT item_name, item_cost FROM menu
                WHERE store_id = ?
                ORDER BY item_cost
        """, (self.id,))
        items = res.fetchall()
        if len(items) == 0:
            raise Exception("No items found")
        return list_to_dict(items)

    def cost(self, item_name: str) -> int | None:
        """
        Finds cost of item
        :parDam item_name: the name of the item
        :return: Either the cost or -1 if the item is not found
        """
        return self.items.get(item_name)


def list_to_dict(l: list[tuple[str, int]]) -> dict[str, int]:
    dictionary: dict[str, int] = {}
    for i, tup in enumerate(l):
        dictionary[tup[0]] = tup[1]
    return dictionary


def get_all_shops() -> dict[str, Shop]:
    con_local, cur_local = link_connection()

    res = cur_local.execute("SELECT DISTINCT store_id FROM menu")
    shop_ids: list[tuple[str]] = res.fetchall()
    # print(shops)
    shops: dict[str, Shop] = {}
    for pos, id in enumerate(shop_ids):
        shops[id[0]] = Shop(id[0])

    return shops


def cleanup() -> None:
    Shop.con.close()


# testing purposes
def print_shop_items(id: str) -> None:
    shop = Shop(id)
    print(shop.items)
    print(shop.cost("item1"))


def main() -> None:
    # test cases
    create_tables()
    print_shop_items('1')

    get_all_shops()
    # raise NotImplementedError
    pass


if __name__ == "__main__":
    main()
