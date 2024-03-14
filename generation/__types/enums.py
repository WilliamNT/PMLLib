from enum import Enum

class ImageSampler(str, Enum):
    """
    Holds various image generation sampler names.
    """

    DPMPP_2M_KARRAS = "DPM++ 2M Karras"
    EULER_ANCESTRAL = "Euler a"
    DDIM = "DDIM"
    PLMS = "PLMS"
    DPMPP_SDE_KARRAS = "DPM++ SDE Karras"
    UNIPC = "UniPC"
    LCM = "LCM"
    EULER_A_SUBSTEP = "Euler A Substep"
    DPMPP_SDE_SUBSTEP = "DPM++ SDE Substep"

    def __str__(self) -> str:
        return self.value
    
class ChatRole(str, Enum):
    """
    Holds the possible chat message author roles.
    """

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

    def __str__(self) -> str:
        return self.value