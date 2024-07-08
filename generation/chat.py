from typing import Optional
import aiohttp
from .types.contracts import GeneratorContract
from .types.structs import ChatModel, GenerationInput, GenerationOutput
from ..utils.service import AsyncService
from .types.exceptions import ServiceBusyException, GenerationAPIException
from datetime import datetime, UTC
from .constants.llm_constants import API_BASE, COMPLETION_ENDPOINT
from .types.structs import ChatMessage, ChatHistory
from .types.enums import ChatRole
from .constants.llm_models import BEST_OVERALL_MODEL

class ChatGenerator(GeneratorContract, AsyncService):
    """
    Handles LLM powered chat responses.

    By default, it is configured to use sensible defaults.
    However, you have the option to provide a custom history object and/or model to use.
    This is useful for maintaining a conversation across multiple requests or using a specific model.
    Otherwise, it will use the best overall model and start a new conversation.
    """

    history = ChatHistory()

    def __init__(self, custom_history: Optional[ChatHistory], model: ChatModel = BEST_OVERALL_MODEL) -> None:
        self.model = model
    
        if custom_history:
            self.history = custom_history
        else:
            self.history.push(ChatMessage(
                role=ChatRole.SYSTEM,
                content=self.model.system_prompt,
                images=None,
            ))

            # Helps to start the conversation.
            self.history.push(ChatMessage(
                role=ChatRole.ASSISTANT,
                content="hi",
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
                    "model": self.model.name, # "llava:7b",
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