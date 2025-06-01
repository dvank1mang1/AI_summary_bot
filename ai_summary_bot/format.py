def format_article(title, summary, source, time):
    return (
        f"📰 <b>{title}</b>\n\n"
        f"{summary}\n\n"
        f"⏰ {time}"
    )
