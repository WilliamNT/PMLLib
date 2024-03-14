from typing import TypeVar, Generic, List, Optional

T = TypeVar("T")

class Stack(Generic[T]):
    """
    An implementation of a stack of `_n_size` size.
    """

    def __init__(self, _n_size: int = 10, _pop_index: int = 0) -> None:
        """
        Initializes a new Stack.
        The default size is 10 but can be supplied via the `_n_size` parameter.
        """
        self._n_size = _n_size
        self._pop_index = _pop_index
        self.items: List[T] = []

    def push(self, item: T) -> None:
        """
        Pushes `item` to the stack.
        """

        if len(self.items) + 1 > self._n_size:
            self.pop(self._pop_index)

        self.items.append(item)

    def pop(self, _index: Optional[int] = None) -> T:
        """
        Pops the item at `_index` from the stack. The default value is `-1`.
        """
        return self.items.pop(self._pop_index if not _index else _index)
    
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