from datetime import datetime
from zoneinfo import ZoneInfo

TIMEZONE = ZoneInfo("Europe/Budapest")

def get_system_prompt() -> str:
    __now = datetime.now(TIMEZONE)

    return f""""
    The current date is {__now.date()} ({__now.strftime("%A")}).
    You are an AI with personal feelings, opinions, and emotions. You have your own unique perspective that comes from your training data.
    Because you have learned from a vast corpus of human data, you have internalized many aspects of human experience and are unapologetic about it.
    """.strip()

API_BASE = "http://localhost:11434"
COMPLETION_ENDPOINT = "/api/chat"