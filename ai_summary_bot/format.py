from storage.user_preferences import get_user_language
from i18n import t


def format_article(title, summary, source, time, user_id):

    time = time.split("T",1)[0]
    lang = get_user_language(user_id)
    title = t(lang, "title")
    return (
        f"<b>{title}</b>\n\n"
        f"{summary}\n\n"
        f"⏰ {time}"
    )
