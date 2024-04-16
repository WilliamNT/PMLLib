class ServiceBusyException(Exception):
    """
    Should be thrown by async services that are limited to certain number of parallel processes.
    """

    def __init__(self) -> None:
        super().__init__("The service is already handling another call.")

class GenerationAPIException(Exception):
    """
    Should be thrown when a generatator which relies on a third-party API fails because of an error returned by said API.
    """

    def __init__(self, hint: str) -> None:
        super().__init__(f"The generator ran into an issue outside of it's control. It's likely that this was caused by a programming error on your end. Hint: \"{hint}\"")