import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def translation(text: str, target_lang: str) -> str:
    prompt = (
        f"Translate the following news summary to {target_lang.upper()}.\n\n"
        f"Text:\n{text}"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a professional translator of news summaries. Mention all slang words, stable expressions and collocations. You should translate without missing a conception and idea"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()
