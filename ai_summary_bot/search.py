from __future__ import annotations

import asyncio
import functools
import os
from typing import List, Tuple

from serpapi import GoogleSearch

_SERP_KEY = os.getenv("SERPAPI_KEY")

def _external_only(results, banned=("t.me", "telegram")):
    clean = []
    for title, link, snip in results:
        if any(b in link for b in banned):
            continue
        clean.append((title, link, snip))
    return clean

def _search_sync(query: str, limit: int) -> List[Tuple[str, str, str]]:
    if not _SERP_KEY:
        raise RuntimeError("SERPAPI_KEY env missing")

    params = {
        "q": query,
        "api_key": _SERP_KEY,
        "num": limit,
        "hl": "ru",
        "gl": "ru",
    }
    results = GoogleSearch(params).get_dict()
    organic = results.get("organic_results", [])[: limit * 2]
    items = [(o["title"], o["link"], o.get("snippet", "")) for o in organic]
    return _external_only(items)[:limit]


async def serpapi_search(query: str, limit: int = 3):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None, functools.partial(_search_sync, query, limit)
    )
