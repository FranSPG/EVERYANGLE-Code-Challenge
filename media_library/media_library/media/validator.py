from typing import Optional

from sqlalchemy.orm import Session


async def verify_category_exist(category_name: str) -> bool:
    if category_name.lower() in ['movies', 'music', 'games']:
        return True
    else:
        return False
