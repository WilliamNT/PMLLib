from dataclasses import dataclass, field
from typing import Optional, Union, Dict, Generic, TypeVar
from datetime import timedelta
from ..constants import img_constants
from .enums import ImageSampler, ChatRole

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

    seed: Optional[str]
    """If applicable, the generation seed used to generate this resource."""

    duration: Optional[timedelta]
    """The duration of the generation."""

    data: T = field(repr=False)
    """The raw generated resource of type `T`. It's up to the user to parse this data."""

    extra: Optional[Dict[str, Union[str, float, int, bool]]] = field(repr=False)
    """Custom additional details about the output."""

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

@dataclass(init=True, repr=True, frozen=True)
class ImageSize:
    """
    Defines the dimensions of an image.
    """

    width: int
    height: int

@dataclass(repr=True, frozen=True)
class ImageModel:
    """
    Is used to define settings for image generation models.
    """

    __default_seed = -1

    def __init__(
            self,
            id: str,
            model: str,
            __refiner_model: str = "",
            steps: Optional[int] = 20,
            __negative_prompt: str = img_constants.GENERAL_NEGATIVE_PROMPT,
            dimensions: ImageSize = ImageSize(512, 512),
            guidance_scale: int = 5.5,
            sampler: ImageSampler = ImageSampler.EULER_ANCESTRAL,
            __default_seed: int = -1,
            __seed_mode: str = "Scale Alike",
            __refiner_start: float = 0.85
    ) -> None:
        self.id = id
        """A unique identifier for the model."""

        self.model = model
        """The model filename."""

        self.refiner_model = __refiner_model
        """An optional refiner model filename."""

        self.steps = steps
        """How many steps the generation should take."""

        self.negative_prompt = __negative_prompt
        """A general negative prompt to let the user define what they don't want to see in the final image."""

        self.dimensions = dimensions
        """The dimensions of the generated image."""
        
        self.guidance_scale = guidance_scale
        """Guidance scale for generation."""

        self.sampler = sampler
        """Which sampler to use."""

        self.default_seed = __default_seed
        """Lets you predefine a default seed for when the user doesn't explicitly pass one as an argument."""

        self.seed_mode = __seed_mode
        """Seed mode."""

        self.refiner_start = __refiner_start
        """If a refiner was specified, at what percentage to start using itit."""

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

    def to_json(self):
        return {
            "role": self.role,
            "content": self.content
        }
    
    @classmethod
    def from_ollama_response(cls, payload: Dict[str, str]):
        return ChatMessage(
            role=payload["message"]["role"],
            content=payload["message"]["content"].strip()
        )