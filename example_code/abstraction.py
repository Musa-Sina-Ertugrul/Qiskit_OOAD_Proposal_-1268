from typing import Type, Any, TypeVar
from abc import abstractmethod, ABCMeta, ABC
from time import sleep
from copy import copy, deepcopy
from enum import Enum

T = TypeVar("T")


def singleton(cls):
    def inner_singleton(cls):
        if hasattr(singleton, "cls"):
            return singleton.cls
        singleton.cls = cls()
        return singleton.cls

    return inner_singleton(cls)


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


class IToastable(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "overlook")
            and callable(subclass.overlook)
            and hasattr(subclass, "bite")
            and callable(subclass.bite)
            or NotImplemented
        )

    @abstractmethod
    def overlook():
        raise NotImplementedError

    @abstractmethod
    def bite():
        raise NotImplementedError


class IToastableWithNoPublicConstructor(type, metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "overlook")
            and callable(subclass.overlook)
            and hasattr(subclass, "bite")
            and callable(subclass.bite)
            or NotImplemented
        )

    @abstractmethod
    def overlook():
        raise NotImplementedError

    @abstractmethod
    def bite():
        raise NotImplementedError

    def __call__(cls, *args, **kwargs):
        raise TypeError(
            f"{cls.__module__}.{cls.__qualname__} has no public constructor"
        )

    def _create(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        return super().__call__(*args, **kwargs)  # type: ignore


class Topping(ABC, metaclass=IToastableWithNoPublicConstructor):
    def __init__(self, next: "Topping") -> None:
        super(ABC, self).__init__()
        self.__name = ""
        self.__builder: "ToppingBuilder" = ToppingBuilder()
        self.__next = None

        @singleton
        class ToppingBuilder:
            def __init__(self):
                self.__Prototypes: dict = {} # add predefined objects

            def add_prototype(self, name: str, prototype: "Topping"):
                if self.__Prototypes.get(name, False):
                    return
                self.__Prototypes[name] = prototype

            def get_prototype(self, name: str) -> "Topping":
                try:
                    return deepcopy(self.__Prototypes[name])
                except ValueError:
                    raise "wrong key"

            def get_prototype_list(self, names: list) -> list:
                result: list = []

                for name in names:
                    result.append(self.get_prototype(name))

                for i in range(len(result) - 1):
                    result[i].__set_next = result[i + 1].next

                return result

    @property
    def name(self):
        return self.__name

    @property
    def next(self):
        return self.__next

    @next
    def __set_next(self, next: "Topping"):
        self.next = next

    def __str__(self):
        return self.__name

    def overlook(self) -> list:
        tmp_next: "Topping" = self.next
        result: list = []
        while tmp_next:
            # NOTE: Do Something like printing names
            sleep(1)
            result.append(tmp_next.name)
            tmp_next = tmp_next.next
        return result

    def add_prototype(self, name: str, prototype: "Topping"):
        self.__builder.add_prototype(name, prototype)

    def make(self, name_key: str):
        self.__builder.get_prototype(name_key)

    def make_list(self, name_keys: list) -> list:
        if any([isinstance(key, str) for key in name_keys]):
            raise ValueError("wrong type")

        return self.__builder.get_prototype_list(name_keys)

    @abstractmethod
    def bootstrap(self):
        raise NotImplementedError

    @abstractmethod
    def bite(self):
        raise NotImplementedError


class ToastBreadState(Enum):
    LIST = 1
    LINKED_LIST = 2


class ToastBread(IToastable):
    def __init__(self, ingredients: Topping | list):
        self.__state = (
            ToastBreadState.LIST
            if isinstance(ingredients, list)
            else ToastBreadState.LINKED_LIST
        )
        self.__ingredients: Topping | list = ingredients

    def setToast(self):
        match self.__state:
            case ToastBreadState.LIST:
                return self.__set_toast_list
            case ToastBreadState.LINKED_LIST:
                return self.__set_toast_linked_list
            case _:
                raise ValueError("Undefined State")

    def __set_toast_linked_list(self):
        # set head of llist with self
        pass

    def __set_toast_list(self):
        # set ingredients
        pass

    def overlook(self):
        match self.__state:
            case ToastBreadState.LIST:
                return self.__overlook_list
            case ToastBreadState.LINKED_LIST:
                return self.__overlook_linked_list
            case _:
                raise ValueError("Undefined State")

    def __overlook_list(self):
        # get names as str list with toast bread
        pass

    def __overlook_linked_list(self):
        # get names as str list with toast bread
        pass

    def __reach_next(self):
        match self.__state:
            case ToastBreadState.LIST:
                return self.__reach_next_list
            case ToastBreadState.LINKED_LIST:
                return self.__reach_next_linked_list
            case _:
                raise ValueError("Undefined State")

    def __reach_next_list(self):
        # return next element with yield
        pass

    def __reach_next_linked_list(self):
        # return next node with yield
        pass


class Custom(Topping, ABC, metaclass=NoPublicConstructor):
    def __init__(self, next: Topping):
        super(Topping, self).__init__(next)
        ABC.__init__(Custom, self)

    @abstractmethod
    def bootstrap():
        raise NotImplementedError

    @abstractmethod
    def bite(self):
        raise NotImplementedError


class ICuttable(type, metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "cut")
            and callable(subclass.cut)
            and hasattr(subclass, "cook")
            and callable(subclass.cook)
            and hasattr(subclass, "bite_deep")
            and callable(subclass.bite_deep)
            and hasattr(subclass, "bite_small")
            and callable(subclass.bite_small)
            and hasattr(subclass, "wait_till_warm")
            and callable(subclass.wait_till_warm)
            or NotImplemented
        )

    @abstractmethod
    def cut(self):
        raise NotImplementedError

    @abstractmethod
    def cook(self):
        raise NotImplementedError

    @abstractmethod
    def bite_deep(self):
        raise NotImplementedError

    @abstractmethod
    def bite_small(self):
        raise NotImplementedError

    @abstractmethod
    def wait_till_warm(self):
        raise NotImplementedError

    def __call__(cls, *args, **kwargs):
        raise TypeError(
            f"{cls.__module__}.{cls.__qualname__} has no public constructor"
        )

    def _create(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        return super().__call__(*args, **kwargs)  # type: ignore


class Sausage(Topping, ABC, metaclass=ICuttable):
    def __init__(self, next: Topping):
        super(Topping, self).__init__(next)
        ABC.__init__(Sausage, self)

    def bootstrap(self):
        self.cut()
        self.cook()
        return self

    def bite(self):
        self.wait_till_warm()
        self.bite_deep()
        self.bite_small()

    @abstractmethod
    def cut(self):
        raise NotImplementedError

    @abstractmethod
    def cook(self):
        raise NotImplementedError

    @abstractmethod
    def wait_till_warm(self):
        raise NotImplementedError

    @abstractmethod
    def bite_deep(self):
        raise NotImplementedError

    @abstractmethod
    def bite_small(self):
        raise NotImplementedError


class Cheese(Topping, ABC, metaclass=ICuttable):
    def __init__(self, next: Topping):
        super(Topping, self).__init__(next)
        ABC.__init__(Cheese, self)

    def bootstrap(self):
        self.cut()
        self.melt()
        return self

    def bite(self):
        self.wait_till_warm()
        self.bite_deep()
        self.pull()
        self.bite_small()

    @abstractmethod
    def cut(self):
        raise NotImplementedError

    @abstractmethod
    def melt(self):
        raise NotImplementedError

    @abstractmethod
    def wait_till_warm(self):
        raise NotImplementedError

    @abstractmethod
    def bite_deep(self):
        raise NotImplementedError

    @abstractmethod
    def bite_small(self):
        raise NotImplementedError

    @abstractmethod
    def pull(self):
        raise NotImplementedError


class Tomato(Topping, ABC, metaclass=ICuttable):
    def __init__(self, next: Topping):
        super(Topping, self).__init__(next)
        ABC.__init__(Tomato, self)

    def bootstrap(self):
        self.cut()
        self.wait_sun()
        self.dry()
        return self

    def bite(self):
        self.wait_till_warm()
        self.bite_deep()
        self.bite_small()

    @abstractmethod
    def cut(self):
        raise NotImplementedError

    @abstractmethod
    def wait_sun(self):
        raise NotImplementedError

    @abstractmethod
    def dry(self):
        raise NotImplementedError

    @abstractmethod
    def wait_till_warm(self):
        raise NotImplementedError

    @abstractmethod
    def bite_deep(self):
        raise NotImplementedError

    @abstractmethod
    def bite_small(self):
        raise NotImplementedError


class Salad(Topping, ABC, metaclass=ICuttable):
    def __init__(self, next: Topping):
        super(Topping, self).__init__(next)
        ABC.__init__(Salad, self)

    def bootstrap(self):
        self.cut_herbs()
        self.cut()
        self.mix()
        return self

    def bite(self):
        self.bite_deep()
        self.bite_small()

    @abstractmethod
    def cut(self):
        raise NotImplementedError

    def cook(self):
        pass

    def wait_till_warm(self):
        pass

    @abstractmethod
    def bite_deep(self):
        raise NotImplementedError

    @abstractmethod
    def bite_small(self):
        raise NotImplementedError

    @abstractmethod
    def mix(self):
        raise NotImplementedError

    @abstractmethod
    def cut_herbs(self):
        raise NotImplementedError


class IPourlable(type, metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "pour")
            and callable(subclass.pour)
            and hasattr(subclass, "add_water")
            and callable(subclass.add_water)
            and hasattr(subclass, "bite_small")
            and callable(subclass.bite_small)
            or NotImplemented
        )

    @abstractmethod
    def pour(self):
        raise NotImplementedError

    @abstractmethod
    def add_water(self):
        raise NotImplementedError

    @abstractmethod
    def bite_small(self):
        raise NotImplementedError

    def __call__(cls, *args, **kwargs):
        raise TypeError(
            f"{cls.__module__}.{cls.__qualname__} has no public constructor"
        )

    def _create(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        return super().__call__(*args, **kwargs)  # type: ignore

class Sauce(Topping,ABC, metaclass=IPourlable):

    def __init__(self, next: Topping) -> None:
        super(Topping,self).__init__(next)
        ABC.__init__(Sauce, self)

    def bite(self):
        self.pour()
        self.bite_small()
    
    def bootstrap(self):
        self.add_water()
        self.mix()
    
    def add_water(self):
        pass

    def pour(self):
        pass

    @abstractmethod
    def mix(self):
        raise NotImplementedError

    @abstractmethod
    def bite_small(self):
        raise NotImplementedError