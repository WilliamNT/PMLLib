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
        self.__default_system_prompt_entry = ChatMessage(
            role=ChatRole.SYSTEM,
            content=self.model.system_prompt,
            images=None,
        )
        self.__default_conversation_starter_entry = ChatMessage(
            role=ChatRole.ASSISTANT,
            content="hi",
            images=None,
        )
    
        if custom_history:
            self.history = custom_history
        else:
            self.history.push(self.__default_system_prompt_entry)
            self.history.push(self.__default_conversation_starter_entry)

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
    
    def replace_history(self, history: ChatHistory) -> None:
        """
        Overrides the current history object with a new one.

        Please note that this replaces the current history object but
        doesn't inject a system prompt.
        """

        self.history = history

    def reset_history(self) -> None:
        """
        Resets the conversation history (makes the LLM forget everything) so the LLM behaves
        just like it would when starting a new conversation.
        """

        self.history = ChatHistory()
        self.history.push(self.__default_system_prompt_entry)
        self.history.push(self.__default_conversation_starter_entry)

    def append_to_history(self, message: ChatMessage) -> None:
        """
        Appends the provided message to the conversation history.
        """

        self.history.push(message)

    async def summarize_history(self, history: Optional[ChatHistory], assistant_name: Optional[str] = "Assistant") -> str:
        """
        Returns an LLM generated summary of the conversation history.
        If no history is provided, it will use the current history object.
        """

        if await self.get_busyness():
            raise ServiceBusyException()
        
        self.set_busyness(True)
        start_stamp = datetime.now(UTC)

        history = history if history else self.history
        history_as_string = "\n".join([message.content for message in history.items])

        prompt = f"""
        You are a language model that has been trained on a large corpus of text data.
        You should write a short and consise description about the relationship between {assistant_name} and each other person.
        You are instructing an actor who is playing the role of {assistant_name}.
        Wording should be present simple.
        Follow the style of this example: "You are {assistant_name}... You have these experiences with these people:"
        Only include details about the conversation and its themes and subjects.

        This is the conversation:
        {history_as_string}
        """

        async with aiohttp.ClientSession() as session:
            async with session.post(url=API_BASE + "/api/generate", json={
                    "model": self.model.name, # "llava:7b",
                    "prompt": prompt,
                    "stream": False,
                }) as generation_req:
                    gen_resp: dict = await generation_req.json()

        if "error" in gen_resp.keys():
            self.set_busyness(False)
            raise GenerationAPIException(gen_resp["error"])

        self.set_busyness(False)
        end_stamp = datetime.now(UTC)
        
        return GenerationOutput[str](
            prompt=prompt,
            model_name=self.model.name,
            duration=(end_stamp - start_stamp),
            data=str(gen_resp["response"]),
            extra=gen_resp
        )