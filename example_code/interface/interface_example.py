from abc import ABCMeta


class A(metaclass=ABCMeta):
    def __subclasshook__(self, subclass) -> None:
        return NotImplemented or (
            hasattr(subclass, "dummy_method") and callable(subclass.dummy_method)
        )
