import aiohttp
from .types.contracts import GeneratorContract
from .types.structs import GenerationInput, GenerationOutput
from ..utils.service import AsyncService
from .types.exceptions import ServiceBusyException, GenerationAPIException
from datetime import datetime, UTC
from .constants.llm_constants import get_system_prompt, API_BASE, COMPLETION_ENDPOINT
from .types.structs import ChatMessage, ChatHistory
from .types.enums import ChatRole

class ChatGenerator(GeneratorContract, AsyncService):
    """
    Handles LLM powered chat responses.
    """

    history = ChatHistory()

    def __init__(self, _system_prompt: str = get_system_prompt()) -> None:
        self.history.push(ChatMessage(
            role=ChatRole.SYSTEM,
            content=_system_prompt,
            images=None,
        ))

    async def generate(self, _input: GenerationInput) -> GenerationOutput:
        if await self.get_busyness():
            raise ServiceBusyException()
        
        self.set_busyness(True)
        start_stamp = datetime.now(UTC)

        self.history.push(ChatMessage(
            role=ChatRole.USER,
            content=_input.prompt,
            images=[_input.image] if _input.image else None,
        ))

        async with aiohttp.ClientSession() as session:
            async with session.post(url=API_BASE + COMPLETION_ENDPOINT, json={
                    "model": "llava:7b",
                    "messages": self.history.to_ollama_payload(),
                    "stream": False,
                    "images": [_input.image] if _input.image else None,
                }) as generation_req:
                gen_resp: dict = await generation_req.json()

        if "error" in gen_resp.keys():
            self.set_busyness(False)
            raise GenerationAPIException(gen_resp["error"])
        
        self.history.push(ChatMessage.from_ollama_response(gen_resp))

        self.set_busyness(False)
        end_stamp = datetime.now(UTC)

        return GenerationOutput[str](
            prompt=_input.prompt,
            model_name=_input.model_name,
            duration=(end_stamp - start_stamp),
            data=self.history.get_last().content,
            extra=gen_resp
        )