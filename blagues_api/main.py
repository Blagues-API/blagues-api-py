import aiohttp
import pydantic

from typing import List
from enum import Enum


class BlagueType(str, Enum):
    GLOBAL = "global"
    DEV = "dev"
    DARK = "dark"
    LIMIT = "limit"
    BEAUF = "beauf"
    BLONDES = "blondes"

    def __str__(self):
        return str(self.value)


class Blague(pydantic.BaseModel):
    id: int
    type: BlagueType
    joke: str
    answer: str


class BlaguesAPI:
    def __init__(self, token: str):
        self.token = token
    
    async def random(self, *, disallow: List[str] = None) -> Blague:
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            
            url = "https://www.blagues-api.fr/api/random"

            if disallow is not None:
                params = {"disallow": disallow}
            else:
                params = {}

            headers = {'Authorization': 'Bearer ' + self.token}

            async with session.get(url, params=params, headers=headers) as resp:
                data = await resp.json()
                return Blague.parse_obj(data)
    
    async def random_categorized(self, category: str) -> Blague:
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            
            url = f"https://www.blagues-api.fr/api/type/{category}/random"
            headers = {'Authorization': 'Bearer ' + self.token}

            async with session.get(url, headers=headers) as resp:
                data = await resp.json()
                return Blague.parse_obj(data)
    
    async def from_id(self, id: int) -> Blague:
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            
            url = f"https://www.blagues-api.fr/api/id/{id}"
            headers = {'Authorization': 'Bearer ' + self.token}

            async with session.get(url, headers=headers) as resp:
                data = await resp.json()
                return Blague.parse_obj(data)
