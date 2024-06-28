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

class CountJoke(pydantic.BaseModel):
    count: int

class BlaguesAPI:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://www.blagues-api.fr/api"
        self.headers = {'Authorization': 'Bearer ' + self.token}


    async def _get(self, url: str, params: dict = None) -> dict:
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            async with session.get(self.base_url+url, headers=self.headers, params=params) as resp:
                return await resp.json()

    async def random(self, *, disallow: List[str] = None) -> Blague:
        endpoint = "/random"
        params = {"disallow": disallow} if disallow else {}
        data = await self._get(endpoint, params)

        return Blague.parse_obj(data)

    async def random_categorized(self, category: str) -> Blague:
        endpoint = f"/type/{category}/random"
        data = await self._get(endpoint)

        return Blague.parse_obj(data)

    async def from_id(self, id: int) -> Blague:
        endpoint = f"/id/{id}"
        data = await self._get(endpoint)

        return Blague.parse_obj(data)

    async def count(self) -> CountJoke:
        endpoint = "/count"
        data = await self._get(endpoint)

        return CountJoke.parse_obj(data)
