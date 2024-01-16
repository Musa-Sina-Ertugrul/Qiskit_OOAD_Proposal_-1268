from typing import Any


class A:
    def __init__(self, next_: "A") -> None:
        self.next_ = next_

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self

    def __str__(self) -> str:
        return " --> class A" + " --> " + str(self.next_)


class B(A):
    def __init__(self, next_: A = None) -> None:
        super().__init__(next_)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self

    def __str__(self) -> str:
        return " --> class B" + " --> " + str(self.next_)


class C(A):
    def __init__(self, next_: A = None) -> None:
        super().__init__(next_)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self

    def __str__(self) -> str:
        return " --> class C" + " --> " + str(self.next_)


if __name__ == "__main__":
    print(B(C()))
    print()
    analysis: list = [B(C()) if i % 2 == 0 else "\n" for i in range(5)]
    print(*analysis)
