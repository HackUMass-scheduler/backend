from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/matches"
)
match_db = {
    "match1": {
        "player": "niranjan",
        "winner": "me",
    },
    "match2": {
        "player": "mathirajan",
        "winner": "you",
    },
}


@router.get("/{match_id}")
async def match_info(match_id: str):
    if match_id not in match_db:
        raise HTTPException(status_code=404)
    return {
        "match player": match_db[match_id]["player"],
        "match winner": match_db[match_id]["winner"]
    }
