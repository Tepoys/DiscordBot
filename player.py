from database import link_connection


class Player:
    con, cur = link_connection()

    def __init__(self, *, id: str = None):
        if id is None:
            raise TypeError('Id is None')

        self.id = id


def main() -> None:
    pass


if __name__ == '__main__':
    main()
