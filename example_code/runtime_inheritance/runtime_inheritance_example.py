from typing import Type
from time import sleep

class ParentA:
   
   def greet(self) -> None:
      print("Hi welcome :)")

class ParentB:
   
   def greet(self) -> None:
      print("Hello World")

def get_my_code(base) -> Type["MyCode"]:

    class MyCode(base):

        def __init__(self) -> None:
           super().__init__()

        def talk(self) -> None:
           super().greet()
           sleep(1)
           print("Bye")

    return MyCode

if __name__ == "__main__":
    dummy: Type["MyCode"] = get_my_code(ParentA)()
    dummy.talk()