import aiohttp
from .constants import GeneratorContract
from .types.structs import GenerationInput, GenerationOutput
from utils.service import AsyncService
from .types.exceptions import ServiceBusyException, GenerationAPIException
from datetime import datetime, UTC
from .constants.llm_constants import get_system_prompt, API_BASE, COMPLETION_ENDPOINT
from utils.stack import Stack
from .types.structs import ChatMessage
from .types.enums import ChatRole

class ChatGenerator(GeneratorContract, AsyncService):
    """
    Handles LLM powered chat responses.
    """

    __history = Stack[ChatMessage](25, 1)

    def __init__(self, __system_prompt: str = get_system_prompt()) -> None:
        self.__history.push(ChatMessage(
            role=ChatRole.SYSTEM,
            content=__system_prompt
        ))

    async def generate(self, _input: GenerationInput) -> GenerationOutput:
        if await self.get_busyness():
            raise ServiceBusyException()
        
        self.set_busyness(True)
        start_stamp = datetime.now(UTC)

        self.__history.push(ChatMessage(
            role=ChatRole.USER,
            content=_input.prompt
        ))

        async with aiohttp.ClientSession() as session:
            async with session.post(url=API_BASE + COMPLETION_ENDPOINT, json={
                    "model": "llama2-uncensored",
                    "messages": self.chat_history.to_ollama_payload(),
                    "stream": False,
                }) as generation_req:
                gen_resp: dict = await generation_req.json()

        if "error" in gen_resp.keys():
            raise GenerationAPIException()
        
        self.__history.push(ChatMessage.from_ollama_response(gen_resp))

        self.set_busyness(False)
        end_stamp = datetime.now(UTC)

        return GenerationOutput[str](
            prompt=_input.prompt,
            model_name=_input.model_name,
            duration=(end_stamp - start_stamp),
            data=self.__history.get_last().content,
            extra=gen_resp
        )