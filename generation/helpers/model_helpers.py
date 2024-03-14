from typing import List, Optional
from generation.__types.structs import ImageModel
from generation.__constants.diffusion_models import MODELS as DIFFUSION_MODELS

def find_model_by_id(id: str, __fallback: ImageModel, __models: List[ImageModel] = DIFFUSION_MODELS) -> Optional[ImageModel]:
    """
    Iterates over the (provided) models and returns the first match.
    Optionally accepts a `__fallback` value which will be returned if no match was found instead of `None`.
    """

    for m in __models:
        if m.id.lower() == id.lower():
            return m
    return None if not __fallback else __fallback
