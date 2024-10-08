from dataclasses import dataclass, field
from typing import List, Optional, Union, Dict, Generic, TypeVar
from datetime import timedelta

from ...generation.constants.llm_constants import get_system_prompt
from ..constants import img_constants
from .enums import ImageSampler, ChatRole
from ...utils.stack import Stack

T = TypeVar("T")

@dataclass(init=True, repr=True, frozen=True)
class GenerationOutput(Generic[T]):
    """
    Standard generation output dataclass to be returned by generator classes.
    """
    
    prompt: str
    """Prompt used to generate this resource."""

    model_name: str
    """Model used to generate this resource."""

    data: T = field(repr=False)
    """The raw generated resource of type `T`. It's up to the user to parse this data."""

    extra: Optional[Dict[str, Union[str, float, int, bool]]] = field(repr=False)
    """Custom additional details about the output."""

    seed: Optional[str] = None
    """If applicable, the generation seed used to generate this resource."""

    duration: Optional[timedelta] = None
    """The duration of the generation."""

@dataclass(init=True, repr=True, frozen=True)
class GenerationInput:
    """
    Basic generation input dataclass.
    """

    prompt: str
    """The prompt the resource should be generated from."""

    model_name: Optional[str]
    """The ML model's optional name or identifier to be used to generate the resource."""

    seed: Optional[str]
    """If applicable, the generation seed to be used to generate the resource."""

    image: Optional[str] = None
    """Optional base64 encoded image data that models that support image input can use."""

@dataclass(init=True, repr=True, frozen=True)
class ImageSize:
    """
    Defines the dimensions of an image.
    """

    width: int
    height: int

@dataclass(repr=True)
class ImageModel:
    """
    Is used to define settings for image generation models.
    """

    __default_seed = -1

    def __init__(
            self,
            _id: str,
            model: str,
            refiner_model: str = "",
            steps: Optional[int] = 20,
            negative_prompt: str = img_constants.GENERAL_NEGATIVE_PROMPT,
            dimensions: ImageSize = ImageSize(512, 512),
            guidance_scale: int = 5.5,
            sampler: ImageSampler = ImageSampler.EULER_ANCESTRAL,
            default_seed: int = -1,
            seed_mode: str = "Scale Alike",
            refiner_start: float = 0.85,
            user_description: str = "This model is a general-purpose image generation model.",
    ) -> None:
        self._id = _id
        """A unique identifier for the model."""

        self.model = model
        """The model filename."""

        self.refiner_model = refiner_model
        """An optional refiner model filename."""

        self.steps = steps
        """How many steps the generation should take."""

        self.negative_prompt = negative_prompt
        """A general negative prompt to let the user define what they don't want to see in the final image."""

        self.dimensions = dimensions
        """The dimensions of the generated image."""
        
        self.guidance_scale = guidance_scale
        """Guidance scale for generation."""

        self.sampler = sampler
        """Which sampler to use."""

        self.default_seed = default_seed
        """Lets you predefine a default seed for when the user doesn't explicitly pass one as an argument."""

        self.seed_mode = seed_mode
        """Seed mode."""

        self.refiner_start = refiner_start
        """If a refiner was specified, at what percentage to start using itit."""

        self.user_description = user_description
        """A user-friendly description of the model."""

    def to_a1_payload(self, prompt: str, __seed: int = __default_seed) -> dict[str, Union[str, int, float]]:
        """
        Returns the model's details in an A1111 compatible JSON object.
        """

        return {
            "prompt": prompt,
            "negative_prompt": self.negative_prompt,
            "steps": self.steps,
            "width": self.dimensions.width,
            "height": self.dimensions.height,
            "model": self.model,
            "seed": __seed,
            "seed_mode": self.seed_mode,
            "guidance_scale": self.guidance_scale,
            "sampler": self.sampler,
            "refiner_start": self.refiner_start,
            "refiner_model": self.refiner_model,
        }
    
@dataclass(init=True, repr=True, frozen=True)
class ChatMessage:
    role: ChatRole
    content: str
    images: Optional[List[str]] = field(repr=False, default=None)

    def to_json(self):
        return {
            "role": self.role,
            "content": self.content,
            "images": self.images if self.images else None
        }
    
    @classmethod
    def from_ollama_response(cls, payload: Dict[str, str]):
        return ChatMessage(
            role=payload["message"]["role"],
            content=payload["message"]["content"].strip()
        )
    
class ChatHistory(Stack[ChatMessage]):
    def __init__(self, _n_size: int = 25, _pop_index: int = 1) -> None:
        super().__init__(_n_size, _pop_index)

    def to_ollama_payload(self) -> List[Dict[str, str]]:
        """
        Returns a list of `ChatMessage` objects serialized to JSON.
        """

        return [msg.to_json() for msg in self.items]
    
@dataclass(repr=True)
class ChatModel:
    """
    Is used to define settings for LLMs.
    """

    def __init__(
            self,
            _id: str,
            name: str,
            is_multimodal: bool = False,
            system_prompt: str = get_system_prompt(),
            allows_nsfw: bool = True,
    ) -> None:
        self._id = _id
        """A unique identifier for the model."""

        self.name = name
        """The model filename."""
        
        self.is_multimodal = is_multimodal
        """Whether the model is multimodal or not. Multimodal models can take image input."""

        self.system_prompt = system_prompt
        """The default system prompt for the model. Usually meant to be overridden."""

        self.allows_nsfw = allows_nsfw
        """Whether the model will refuse to generate NSFW content or not."""