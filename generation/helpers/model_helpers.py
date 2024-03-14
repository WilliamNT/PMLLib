from typing import List, Optional
from ..types.structs import ImageModel
from ..constants.diffusion_models import MODELS as DIFFUSION_MODELS

def find_model_by_id(_id: str, _fallback: ImageModel, _models: List[ImageModel] = DIFFUSION_MODELS) -> Optional[ImageModel]:
    """
    Iterates over the (provided) models and returns the first match.
    Optionally accepts a `__fallback` value which will be returned if no match was found instead of `None`.
    """

    for m in _models:
        if m._id.lower() == _id.lower():
            return m
    return None if not _fallback else _fallback
