from asyncio import Lock

class Service:
    """
    A general descriptive class to define services.
    """

    pass

class AsyncService(Service):
    """
    A general meta class to implement async services.
    """

    __lock: Lock = Lock()

    # Intended to be used when you only want to allow one use at a time.
    __is_busy: bool = False

    async def get_busyness(self) -> bool:
        """
        Returns `True` if the service is busy, otherwise `False`.
        """
        
        async with self.__lock:
            return self.__is_busy
        
    def set_busyness(self, v: bool) -> None:
        self.__is_busy = v

class ServiceBusyException(Exception):
    def __init__(self) -> None:
        super().__init__("The call can't be handled at this time because the service is busy handling another.")