from typing import List
from ...generation.types.structs import ChatModel

LLAMA2_7B = ChatModel(
    _id="llama2",
    name="llama2:7b",
    is_multimodal=False,
    allows_nsfw=False,
)

LLAVA_7B = ChatModel(
    _id="llava7b",
    name="llava:7b",
    is_multimodal=True,
    allows_nsfw=False,
)

LLAMA3_8B = ChatModel(
    _id="llama3",
    name="llama3",
    is_multimodal=False,
    allows_nsfw=False,
)

LLAMA3_8B_UNCENSORED = ChatModel(
    _id="llama3_uncensored",
    name="sunapi386/llama-3-lexi-uncensored:8b",
    is_multimodal=False,
    allows_nsfw=True,
)

BEST_OVERALL_MODEL = LLAMA3_8B_UNCENSORED

MODELS: List[ChatModel] = [
    LLAVA_7B,
    LLAMA2_7B,
    LLAMA3_8B,
    LLAMA3_8B_UNCENSORED,
]