import os
import logging

from googletrans import Translator
import openai
from openai import OpenAIError

translator = Translator()
openai.api_key = os.getenv("OPENAI_API_KEY")
logger = logging.getLogger(__name__)

SYS_PROMPT = {
    "ru": (
        "Отполируй текст: сделай изложение естественным, живым, "
        "допустимы лёгкие эмодзи; сохрани HTML-разметку."
    ),
    "en": (
        "Polish the text so it reads naturally and engagingly in English; "
        "light emojis are allowed. Preserve HTML markup."
    ),
}


def _gpt_polish(text: str, lang: str) -> str:
    if not openai.api_key:
        logger.warning("OPENAI_API_KEY not set → skip polish")
        return text
    try:
        resp = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYS_PROMPT[lang]},
                {"role": "user", "content": text},
            ],
            temperature=0.4,
            max_tokens=int(len(text) * 1.2),
        )
        return resp.choices[0].message.content.strip()
    except OpenAIError as e:
        logger.warning("GPT polish failed: %s", e)
        return text

async def translation(text: str, target_lang: str) -> str:
    if not text or target_lang not in ("ru", "en"):
        return text

    result = await translator.translate(text, dest=target_lang)
    text = result.text

    return _gpt_polish(text, target_lang)
