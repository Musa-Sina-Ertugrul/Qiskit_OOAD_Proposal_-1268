from typing import Any, Optional


class A:
    def __init__(self) -> None:
        self.next = None
    def __call__(self, func : callable,*args: Any, **kwds: Any) -> Any:
        return func,self
    def __str__(self) -> str:
        return " --> class A" + " --> " + str(self.next)
class B:
    def __init__(self) -> None:
        self.next = None
    def __call__(self,func : callable,*args: Any, **kwds: Any) -> Any:
        return func,self
    def __str__(self) -> str:
        return " --> class B" + " --> " + str(self.next)
class C:
    def __init__(self) -> None:
        self.next = None
    def __call__(self,func : callable,*args: Any, **kwds: Any) -> Any:
        return func,self
    def __str__(self) -> str:
        return " --> class C" + " --> " + str(self.next)

@A()
@B()
@C()
def dummy_func() -> None:
    pass

def collect_items(items:tuple,collected_items:list)->list:
    if type(items[0]) != tuple:
        return collected_items.append(items[-1])
    collected_items.append(items[-1])
    return collect_items(items[0],collected_items)

def attach_list(current_list: list) -> None:
    for i in range(len(current_list)-1):
        current_list[i].next = current_list[i+1]

if __name__ == "__main__":

    decarators : list = []
    collect_items(dummy_func,decarators)
    attach_list(decarators)
    print(*decarators)
    print()
    print(*[decarators[0] for _ in range(3)]) # building multi way experiments