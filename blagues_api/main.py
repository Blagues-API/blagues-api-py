from enum import Enum
from typing import List

import aiohttp
import pydantic


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
        self.headers = {"Authorization": f"Bearer {self.token}"}

    async def _get(self, url: str, params: dict = None) -> dict:
        """Make a GET request to the API."""
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            async with session.get(
                self.base_url + url, headers=self.headers, params=params
            ) as resp:
                return await resp.json()

    async def random(self, *, disallow: List[str] = None) -> Blague:
        """
        Get a random joke.
        Usage: random(disallow=['dev', 'dark',...])
        """
        endpoint = "/random"
        params = {"disallow": disallow} if disallow else {}
        data = await self._get(endpoint, params)

        return Blague.model_validate(data)

    async def random_categorized(self, category: str) -> Blague:
        """
        Get a random joke from a specific category.
        Usage: random_categorized(category=BlagueType.DEV)
        """
        endpoint = f"/type/{category}/random"
        data = await self._get(endpoint)

        return Blague.model_validate(data)

    async def from_id(self, id: int) -> Blague:
        """
        Get a joke from its ID.
        Usage: from_id(1)
        """
        endpoint = f"/id/{id}"
        data = await self._get(endpoint)

        return Blague.model_validate(data)

    async def count(self) -> CountJoke:
        """Get the number of jokes available."""
        endpoint = "/count"
        data = await self._get(endpoint)

        return CountJoke.model_validate(data)
