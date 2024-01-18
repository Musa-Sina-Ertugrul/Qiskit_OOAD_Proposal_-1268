from time import sleep
from abc import ABC, abstractclassmethod
from typing import Any


class CommandTemplate(ABC):
    def __init__(self) -> None:
        super().__init__()

    def do_tasks(self) -> None:
        self.task_1()
        self.task_2()
        self.task_3()

    @abstractclassmethod
    def task_1(self) -> None:
        raise NotImplementedError

    @abstractclassmethod
    def task_2(self) -> None:
        raise NotImplementedError

    @abstractclassmethod
    def task_3(self) -> None:
        raise NotImplementedError

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.do_tasks(*args, **kwds)


class A(CommandTemplate):
    def __init__(self) -> None:
        super().__init__()

    def task_1(self) -> None:
        print("Task 1")
        sleep(1)

    def task_2(self) -> None:
        print("Task 2")
        sleep(1)

    def task_3(self) -> None:
        print("Task 3")
        sleep(1)


class B:
    def __init__(self, command: object) -> None:
        self.__command: object = command

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.__command(*args, **kwds)


if __name__ == "__main__":
    dummy: B = B(A())
    dummy()
