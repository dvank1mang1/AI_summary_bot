from telethon import TelegramClient
import asyncio
import re
import os
from dotenv import load_dotenv
from collections import Counter
from ai.bayesian_model import select_important as bayesian_filter
from ai.fdr_model import select_important as fdr_filter
from ai.logreg_model import select_important as logreg_filter
from ai.tfidf_model import select_important as tfidf_filter
from ai.zscore_model import select_important as zscore_filter

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

CHANNELS = [
    '@ChatGPT_BIAbotRUS',
    '@incubeai_pro',
    '@ai2smm',
    '@hiaimedia',
    '@GPTMainNews',
    '@seeallochnaya',
    '@ai_newz',
    '@Artificial_intelligence_in'
]

api_id = int(os.getenv('TG_API_ID'))
api_hash = os.getenv('TG_API_HASH')

client = TelegramClient('ai_news_parser', api_id, api_hash)

MODEL_OPTIONS = {
    'bayesian': bayesian_filter,
    'fdr': fdr_filter,
    'logreg': logreg_filter,
    'tfidf': tfidf_filter,
    'zscore': zscore_filter
}

MODELS_TO_USE = ['fdr']


def clean_text(text):
    """
    Clean the input text by removing URLs, extra spaces, and special characters.
    """
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'[\W_]+', ' ', text)
    return text.strip()


async def fetch_messages(limit_per_channel=30):
    """
    Fetch messages from the specified Telegram channels.
    """
    all_articles = []
    successful_channels = 0
    failed_channels = 0

    async with client:
        for channel in CHANNELS:
            print(f"Channel parsing: {channel}")
            try:
                channel_articles = []
                async for msg in client.iter_messages(channel, limit=limit_per_channel):
                    if msg.text and len(msg.text.strip()) > 5:
                        article = {
                            "channel": channel,
                            "message_id": msg.id,
                            "text": clean_text(msg.text),
                            "date": msg.date,
                            "url": f"https://t.me/{channel[1:]}/{msg.id}"
                        }
                        channel_articles.append(article)

                if channel_articles:
                    print(f"Found {len(channel_articles)} articles in {channel}")
                    successful_channels += 1
                    all_articles.extend(channel_articles)
                else:
                    print(f"Channel {channel} doesn't have appropriate articles")

            except Exception as e:
                print(f"Parsing error {channel}: {e}")
                failed_channels += 1

    print(f"Overall done: {successful_channels}, errors: {failed_channels}")
    return all_articles


def filter_articles(articles):
    """
    Filter articles based on multiple models and perform majority voting.
    """
    # Remove articles without text
    articles = [a for a in articles if a['text']]
    if not articles:
        print("All articles are empty or consist of stop-words!")
        return []

    # Log distribution of articles across channels
    print("=== Channel distribution before filtering ===")
    channel_counts = Counter(a['channel'] for a in articles)

    for channel, count in channel_counts.items():
        print(f"{channel}: {count} articles")

    # Initialize containers
    filtered_results = {}
    model_votes = Counter()

    # Run articles through each model
    for model_name in MODELS_TO_USE:
        model = MODEL_OPTIONS.get(model_name)
        if model:
            print(f"\nSending {len(articles)} articles to {model_name}")
            filtered = model(articles)

            if not filtered:
                print(f"Model {model_name} did not return any articles.")
            else:
                print(f"Model {model_name} returned {len(filtered)} articles.")
            
            # Store results and update votes
            filtered_results[model_name] = filtered

            # Display selected articles per model
            print(f"\n=== Articles selected by {model_name} ===")
            for article in filtered:
                print(f"[{article['date']}] {article['channel']}: {article['text'][:50]}... — {article['url']}")
                model_votes[article['url']] += 1

    # Define majority threshold (ceil to include the majority)
    majority_vote_threshold = (len(MODELS_TO_USE) // 2) + 1
    print(f"\nMajority vote threshold: {majority_vote_threshold}")

    # Select articles that appeared in the majority of models
    final_selection = [article for article in articles if model_votes[article['url']] >= majority_vote_threshold]

    print(f"\nFinal selected articles by majority vote: {len(final_selection)}")
    return final_selection


async def main():
    articles = await fetch_messages()
    print(f"\nTotal articles fetched: {len(articles)}")
    filtered = filter_articles(articles)
    print("\n=== Final Articles ===")
    for article in filtered:
        print(f"[{article['date']}] {article['channel']}: {article['text'][:50]}... — {article['url']}")

if __name__ == "__main__":
    asyncio.run(main())
