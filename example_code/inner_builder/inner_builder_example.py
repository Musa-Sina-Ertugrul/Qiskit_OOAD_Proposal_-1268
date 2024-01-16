from copy import deepcopy
from typing import Optional, TypeVar, Type, Any, Generic, ForwardRef, TypedDict
from dataclasses import dataclass, field
from abc import ABC
from pydantic import BaseModel

T = TypeVar("T")

from typing import Type, Optional


class NoPublicConstructor(type):
    def __call__(cls, *args, **kwargs):
        raise TypeError(f"{cls.__name__} cannot be instantiated directly")

    def _create(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        return super().__call__(*args, **kwargs)  # type: ignore


class A(metaclass=NoPublicConstructor):
    class __Builder:
        __Prototypes: dict = {"B": None, "C": None}

        def __init__(self) -> None:
            pass

        def add_prototype(self, name: str, prototype: Type["A"]) -> None:
            if self.__Prototypes.get(name, False):
                return
            self.__Prototypes[name] = prototype

        def get_prototype(self, name: str) -> "A":
            try:
                return self.__Prototypes[name]._create()
            except ValueError:
                raise ValueError("wrong key")

    __InnerBuilder = __Builder()

    def __init__(self, next_: Type["A"] = None, prev: Type["A"] = None) -> None:
        self.__next: Optional[Type["A"]] = next_
        self.previous: Optional[Type["A"]] = prev

    def next(self, cls_name: str) -> None:
        self.__next = self.__InnerBuilder.get_prototype(cls_name)
        self.__next.previous = self
        return self.__next

    @classmethod
    def build(cls, cls_name: str) -> "A":
        return cls.__InnerBuilder.get_prototype(cls_name)

    def __str__(self) -> str:
        return f"class {self.__class__.__name__} {self.previous}"

    @classmethod
    def add_prototype(cls, added_cls):
        cls.__InnerBuilder.add_prototype(added_cls.__name__, added_cls)


class B(A):
    def __init__(self, next_: type[A] = None, prev: Type["A"] = None) -> None:
        super().__init__(next_, prev)


class C(A):
    def __init__(self, next_: type[A] = None, prev: Type["A"] = None) -> None:
        super().__init__(next_, prev)


A.add_prototype(B)
A.add_prototype(C)

if __name__ == "__main__":
    var = A.build("B").next("C").next("B")
    print(var)
