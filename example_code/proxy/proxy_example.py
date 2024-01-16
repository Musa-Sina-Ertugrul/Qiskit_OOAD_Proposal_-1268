from time import sleep
from typing import Optional


class DataContainer:
    def __init__(self, data: str) -> None:
        self.__data_hash: str = "123xyz123"
        self.__inner_container = self.InnerDataContainer()
        self.__inner_container.add_data(self.__data_hash, data)

    class InnerDataContainer:
        datas: dict = {"123xyz123": "experiment_data"}

        def __init__(self) -> None:
            pass

        def retrive_from_db(self, hash_: str) -> str:
            sleep(5)  # retriving
            return "123xyz123"

        def retrive_data(self, hash_: str) -> str:
            if hash_ in self.datas:
                return self.datas[hash_]
            self.datas[hash_] = self.retrive_from_db(hash_)
            return self.datas[hash_]

        def send_to_db(self, hash_: str, data: str) -> None:
            sleep(5)

        def add_data(self, hash_: str, data: str, cache: bool = False) -> None:
            data: Optional[str] = self.retrive_data(hash_)
            if data:
                return
            if cache:
                self.datas[hash_] = data
            self.send_to_db(hash_, data)

    def __str__(self) -> str:
        return self.__inner_container.retrive_data(self.__data_hash)


if __name__ == "__main__":
    data = DataContainer("Hello")
    print(data)
