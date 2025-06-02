
import os
import openai
from dotenv import load_dotenv
import asyncio

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


async def summarize_with_gpt(base_text: str, size: str, additional_context: str | None = None) -> str:


    if size == "normal":
        prompt = (
            f"Summarize the following news article in 3–5 sentences:\n\n{base_text}"
        )
    elif size == "extended" and additional_context:
        prompt = (
            "You are an expert news summarizer.\n\n"
            "Original news article:\n"
            f"{base_text}\n\n"
            "Additional external information:\n"
            f"{additional_context}\n\n"
            "Generate a detailed, informative summary that integrates both the article and external information. But not use phrases like 'Brief content' and others "
            "Keep it clear, structured, and easy to read."
        )
    else:
        prompt = (
            f"Summarize the following news article:\n\n{base_text}"
        )

   
    client = openai.OpenAI()

    
    response = await asyncio.to_thread(
        client.chat.completions.create,
        model="gpt-3.5-turbo",  
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes news articles."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4,
        max_tokens=512
    )

    
    summary = response.choices[0].message.content.strip()
    return summary
