from howlongtobeatpy import HowLongToBeat
import re
import asyncio

def extract_hltb_id(url: str) -> str | None:
    match = re.search(r'howlongtobeat\.com/game/(\d+)', url)
    return match.group(1) if match else None

async def fetch_hltb_data(hltb_id: str) -> dict | None:
    game = await HowLongToBeat().async_search_from_id(int(hltb_id))
    if not game:
        return None
    return {
        'hltb_id': str(hltb_id),
        'name': game.game_name,
        'cover_url': game.game_image_url,
        'genres': []
    }

def get_hltb_data(url: str) -> dict | None:
    hltb_id = extract_hltb_id(url)
    if not hltb_id:
        return None
    return asyncio.run(fetch_hltb_data(hltb_id))