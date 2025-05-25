from translations import translations

def t(lang: str, key: str, **kwargs) -> str:
    """Get translated string for a given key and language"""
    fallback = translations.get("ru", {})
    lang_dict = translations.get(lang, fallback)
    text = lang_dict.get(key, fallback.get(key, key))
    return text.format(**kwargs)
