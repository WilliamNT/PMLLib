from typing import TypeVar, Generic, List, Optional

T = TypeVar("T")

class Stack(Generic[T]):
    """
    An implementation of a stack of `__n_size` size.
    """

    def __init__(self, __n_size: int = 10, __pop_index: int = 0) -> None:
        """
        Initializes a new Stack.
        The default size is 10 but can be supplied via the `__n_size` parameter.
        """
        self._n_size = __n_size
        self.__pop_index = __pop_index
        self.items: List[T] = []

    def push(self, item: T) -> None:
        """
        Pushes `item` to the stack.
        """

        if len(self.items) + 1 > self.__n_size:
            self.pop(self.__pop_index)

        self.items.append(item)

    def pop(self, __index: Optional[int] = None) -> T:
        """
        Pops the item at `__index` from the stack. The default value is `-1`.
        """
        return self.items.pop(self.__pop_index if not __index else __index)
    
    def is_empty(self) -> bool:
        """
        Returns `True` if the stack is empty and `False` if not.
        """
        return not self.items
    
    def pop_all(self) -> None:
        """
        Pops all items in the stack.
        """
        self.items = []

    def get_first(self) -> Optional[T]:
        """
        Returns the first item in the stack.
        """
        return self.items[0]
    
    def get_last(self) -> Optional[T]:
        """
        Returns the last item in the stack.
        """
        return self.items[-1]