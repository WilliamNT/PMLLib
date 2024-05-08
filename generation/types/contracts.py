from abc import ABC, abstractmethod
from .structs import GenerationInput, GenerationOutput

class GeneratorContract(ABC):
    """
    Defines a contract to be implemented by AI/ML generation classes.
    """

    @abstractmethod
    async def generate(self, _input: GenerationInput) -> GenerationOutput:
        """
        Generates an applicable resource and
        returns it wrapped in a `GenerationOutput` object.

        May raise a `ServiceBusyException` depending on the implemntation.
        """
        
        pass