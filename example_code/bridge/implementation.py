from example_code.bridge.abstraction import Salad, Sauce, Sausage, Cheese, Tomato, NoPublicConstructor
from abc import ABC, ABCMeta, abstractmethod
from typing import Type, Any, TypeVar

from example_code.bridge.abstraction import Topping

T = TypeVar("T")


class ColourfulSausage(Sausage, metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "make_more_red")
            and callable(subclass.make_more_red)
            or NotImplemented
        )

    def __call__(cls, *args, **kwargs):
        raise TypeError(
            f"{cls.__module__}.{cls.__qualname__} has no public constructor"
        )

    def _create(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        return super().__call__(*args, **kwargs)  # type: ignore


class PaleSausage(Sausage, metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "make_more_pale")
            and callable(subclass.make_more_pale)
            or NotImplemented
        )

    def __call__(cls, *args, **kwargs):
        raise TypeError(
            f"{cls.__module__}.{cls.__qualname__} has no public constructor"
        )

    def _create(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        return super().__call__(*args, **kwargs)  # type: ignore


class GermanSausage(ColourfulSausage):
    def __init__(self, next: Topping):
        super().__init__(next)

    def make_more_red(self):
        pass


class PolishSausage(PaleSausage):
    def __init__(self, next: Topping):
        super().__init__(next)

    def make_more_pale(self):
        pass


class BadSmellCheese(Cheese, metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "cover_smell")
            and callable(subclass.cover_smell)
            or NotImplemented
        )

    def __call__(cls, *args, **kwargs):
        raise TypeError(
            f"{cls.__module__}.{cls.__qualname__} has no public constructor"
        )

    def _create(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        return super().__call__(*args, **kwargs)  # type: ignore


class GoodSmellCheese(Cheese, metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "make_more_smelly")
            and callable(subclass.make_more_smelly)
            or NotImplemented
        )

    def __call__(cls, *args, **kwargs):
        raise TypeError(
            f"{cls.__module__}.{cls.__qualname__} has no public constructor"
        )

    def _create(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        return super().__call__(*args, **kwargs)  # type: ignore


class HollandCheese(BadSmellCheese):
    def __init__(self, next: Topping):
        super().__init__(next)

    def cover_smell(self):
        pass


class ItalianCheese(GoodSmellCheese):
    def __init__(self, next: Topping):
        super().__init__(next)

    def make_more_smelly(self):
        pass


class FarmTomato(Tomato, metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "dry_sun")
            and callable(subclass.dry_sun)
            or NotImplemented
        )

    def __call__(cls, *args, **kwargs):
        raise TypeError(
            f"{cls.__module__}.{cls.__qualname__} has no public constructor"
        )

    def _create(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        return super().__call__(*args, **kwargs)  # type: ignore


class GreenHouseTomato(Tomato, metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "dry_oven")
            and callable(subclass.dry_oven)
            or NotImplemented
        )

    def __call__(cls, *args, **kwargs):
        raise TypeError(
            f"{cls.__module__}.{cls.__qualname__} has no public constructor"
        )

    def _create(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        return super().__call__(*args, **kwargs)  # type: ignore


class BigTomato(FarmTomato):
    def __init__(self, next: Topping):
        super().__init__(next)

    def dry(self):
        self.dry_sun()
        super().dry()

    def dry_sun(self):
        pass


class CherryTomato(GreenHouseTomato):
    def __init__(self, next: Topping):
        super().__init__(next)

    def dry(self):
        self.dry_oven()
        super().dry()

    def dry_oven(self):
        pass


class MilkBasedSauce(Sauce, metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "pour_milk")
            and callable(subclass.pour_milk)
            or NotImplemented
        )

    def __call__(cls, *args, **kwargs):
        raise TypeError(
            f"{cls.__module__}.{cls.__qualname__} has no public constructor"
        )

    def _create(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        return super().__call__(*args, **kwargs)  # type: ignore


class TomatoBasedSauce(Sauce, metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "pour_tomato")
            and callable(subclass.pour_tomato)
            or NotImplemented
        )

    def __call__(cls, *args, **kwargs):
        raise TypeError(
            f"{cls.__module__}.{cls.__qualname__} has no public constructor"
        )

    def _create(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        return super().__call__(*args, **kwargs)  # type: ignore


class MayoSauce(MilkBasedSauce):
    def __init__(self, next: Topping) -> None:
        super().__init__(next)

    def pour_milk(self):
        pass

    def pour(self):
        self.pour_milk()
        super().pour()


class Ketchup(TomatoBasedSauce):
    def __init__(self, next: Topping) -> None:
        super().__init__(next)

    def pour_tomato(self):
        pass

    def pour(self):
        self.pour_tomato()
        super().pour()


class RefreshingSalad(Salad, metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "mix_herbs")
            and callable(subclass.mix_herbs)
            or NotImplemented
        )

    def __call__(cls, *args, **kwargs):
        raise TypeError(
            f"{cls.__module__}.{cls.__qualname__} has no public constructor"
        )

    def _create(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        return super().__call__(*args, **kwargs)  # type: ignore


class FishwSalad(Salad, metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "cut_fish")
            and callable(subclass.cut_fish)
            and hasattr(subclass, "mix_herbs_fish")
            and callable(subclass.mix_herbs_fish)
            or NotImplemented
        )

    def __call__(cls, *args, **kwargs):
        raise TypeError(
            f"{cls.__module__}.{cls.__qualname__} has no public constructor"
        )

    def _create(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        return super().__call__(*args, **kwargs)  # type: ignore


class WhiteSeaSalad(RefreshingSalad):
    def __init__(self, next: Topping):
        super().__init__(next)

    def mix_herbs(self):
        pass

    def mix(self):
        self.mix_herbs()
        super().mix()


class TunaSalad(FishwSalad):
    def __init__(self, next: Topping):
        super().__init__(next)

    def mix_herbs_fish(self):
        pass

    def mix(self):
        self.mix_herbs_fish()
        super().mix()

    def cut_fish(self):
        pass

    def cut(self):
        self.cut_fish()
        super().cut()
