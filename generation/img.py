from aiohttp import ClientSession
from .types.contracts import GeneratorContract
from .types.structs import GenerationInput, GenerationOutput
from utils.service import AsyncService
from .types.exceptions import ServiceBusyException, GenerationAPIException
from .types.structs import ImageModel
from generation.helpers.model_helpers import find_model_by_id
from .constants.diffusion_models import BEST_OVERALL_MODEL
from .constants.img_constants import API_BASE, TXT2IMG_ENDPOINT
from datetime import datetime, UTC
from typing import Dict, Union
from io import BytesIO
import base64

class ImageGenerator(GeneratorContract, AsyncService):
    """
    Handles image generation.
    """

    async def generate(self, _input: GenerationInput) -> GenerationOutput:
        if await self.get_busyness():
            raise ServiceBusyException()
        
        self.set_busyness(True)
        start_stamp = datetime.now(UTC)

        model: ImageModel = find_model_by_id(_input.model_name, BEST_OVERALL_MODEL)
        
        async with ClientSession() as s:
           async with s.post(url=API_BASE + TXT2IMG_ENDPOINT, json=model.to_a1_payload(_input.prompt, _input.seed)) as gen_req:
               image_data = await gen_req.json()
    
               if dict(image_data).get("error", None):
                   raise GenerationAPIException()
               
           async with s.get(API_BASE) as details_req:
               details: Dict[str, Union[str, int, float, bool]] = dict(await details_req.json())


        image_bytes = base64.b64decode(list(image_data.get("images"))[0])
        image_binary = BytesIO(image_bytes)
        image_binary.seek(0)

        self.set_busyness(False)
        end_stamp = datetime.now(UTC)
        
        return GenerationOutput[BytesIO](
            prompt=_input.prompt,
            model_name=model.model,
            seed=_input.seed,
            duration=(end_stamp - start_stamp),
            data=image_binary,
            extra=details
        )
    