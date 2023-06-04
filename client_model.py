from framework.types.types import DbModel, Mapper, MapperRegistry


class Client(DbModel):
    tablename = "client"
    id: int
    login: str
    passwd: bytearray

    def __init__(self, id, login, passwd) -> None:
        super().__init__()
        self.id = id
        self.login = login
        self.passwd = passwd

    def is_auth(self):
        return True

    def __str__(self) -> str:
        return f"Client[{self.id}]{self.login}"

    def __repr__(self) -> str:
        return f"Client[{self.id}]{self.login}"


class ClientMapper(Mapper):
    model = Client
    tablename = "client"

    def insert(self, obj):
        return super().insert(obj, ("login", "passwd"))

    def update(self, obj):
        return super().update(obj, {"login": obj.login, "passwd": obj.passwd})
