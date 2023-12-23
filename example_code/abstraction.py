from typing import Type, Any, TypeVar
from abc import abstractmethod, ABCMeta, ABC
from time import sleep
from copy import copy, deepcopy
from enum import Enum
T = TypeVar("T")

def singleton(cls):

    def inner_singleton(cls):

        if hasattr(singleton,"cls"):
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
        return hasattr(subclass, "overlook") and callable(subclass.overlook) and hasattr(subclass, "bite") and callable(subclass.bite) or NotImplemented

    @abstractmethod
    def overlook():
        raise NotImplementedError
    
    @abstractmethod
    def bite():
        raise NotImplementedError

class Topping(ABC,IToastable,metaclass=NoPublicConstructor):

    def __init__(self,next : "Topping") -> None:
        ABC.__init__(Topping,self)
        self.__name = ""
        self.__builder : "ToppingBuilder" = ToppingBuilder()
        self.__next = None
    
        @singleton
        class ToppingBuilder:

            def __init__(self):
                self.__Prototypes : dict = {

                }

            def add_prototype(self,name:str,prototype:"Topping"):
                if self.__Prototypes.get(name,False):
                    return
                self.__Prototypes[name] = prototype.bootstrap()
            
            def get_prototype(self,name:str)->"Topping":
                try:
                    return deepcopy(self.__Prototypes[name])
                except ValueError:
                    raise "wrong key"
            
            def get_prototype_list(self,names : list) -> list:

                result : list = []

                for name in names:
                    result.append(self.get_prototype(name))
                
                for i in range(len(result)-1):
                    result[i].__set_next = result[i+1].next
                
                return result

    @property
    def name(self):
        return self.__name
    
    @property
    def next(self):
        return self.__next
    
    @next
    def __set_next(self,next : "Topping"):
        self.next = next

    def __str__(self):
        return self.__name

    def overlook(self) -> list:
        tmp_next : "Topping" = self.next
        result : list = []
        while tmp_next:
            # NOTE: Do Something like printing names
            sleep(1)
            result.append(tmp_next.name)
            tmp_next = tmp_next.next
        return result

    def add_prototype(self,name:str,prototype:"Topping"):
        self.__builder.add_prototype(name,prototype)
    
    def make(self,name_key : str):
        self.__builder.get_prototype(name_key)

    def make_list(self,name_keys:list) -> list:

        if any([isinstance(key,str) for key in name_keys]):
            raise ValueError("wrong type")
        
        return self.__builder.get_prototype_list(name_keys)
    
    @abstractmethod
    def bootstrap():
        raise NotImplementedError

    @abstractmethod
    def bite(self):
        raise NotImplementedError
            
class ToastBreadState(Enum):
    LIST = 1
    LINKED_LIST = 2

class ToastBread(IToastable):

    def __init__(self,ingredients: Topping | list):
        self.__state = ToastBreadState.LIST if isinstance(ingredients,list) else ToastBreadState.LINKED_LIST
        self.__ingredients : Topping | list = ingredients