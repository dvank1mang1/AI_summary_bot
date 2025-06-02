def format_article(title, summary, source, time):
    time = time.split("T",1)[0]
    return (
        f"📰 <b>{title}</b>\n\n"
        f"{summary}\n\n"
        f"⏰ {time}"
    )
