from copy import deepcopy
from typing import TypeVar,Type,Any

T = TypeVar("T")

class NoPublicConstructor(type):
    """Metaclass that ensures a private constructor

    If a class uses this metaclass like this:

        class SomeClass(metaclass=NoPublicConstructor):
            pass

    If you try to instantiate your class (`SomeClass()`),
    a `TypeError` will be thrown.
    """

    def __call__(cls, *args, **kwargs):
        raise TypeError(
            f"{cls.__module__}.{cls.__qualname__} has no public constructor"
        )

    def _create(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        return super().__call__(*args, **kwargs)  # type: ignore


class B(metaclass=NoPublicConstructor):
    
    def __init__(self) -> None:
        pass
    
    def __str__(self) -> str:
        return "class B"

class A(metaclass=NoPublicConstructor):

    class __Builder:
            Prototypes: dict = {
                "B" : B._create()
            } # add predefined objects
            def __init__(self) -> None:
                if not "B" in self.Prototypes:
                    B._create()

            def add_prototype(self, name: str, prototype: "Topping") -> None:
                if self.__Prototypes.get(name, False):
                    return
                self.__Prototypes[name] = prototype

            def get_prototype(self, name: str) -> "Topping":
                try:
                    return deepcopy(self.Prototypes[name])
                except ValueError:
                    raise "wrong key"

            def get_prototype_list(self, names: list) -> list:
                result: list = []

                for name in names:
                    result.append(self.get_prototype(name))

                for i in range(len(result) - 1):
                    result[i].__set_next = result[i + 1].next

                return result

    __Builder = __Builder()

    def __init__(self) -> None:
        self.builder = self.__Builder

    @classmethod
    def build(cls,cls_name : str) -> Any:
        return cls._create().builder.get_prototype(cls_name)

if __name__ == "__main__":
    print(A.build("B"))