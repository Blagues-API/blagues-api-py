import pytest
from dotenv import load_dotenv
import os

from blagues_api import Blague, BlaguesAPI, BlagueType, CountJoke

pytestmark = pytest.mark.asyncio

load_dotenv()


@pytest.fixture
def token():
    return os.getenv("TOKEN")


@pytest.fixture
def client(token):
    return BlaguesAPI(token)


async def test_random_joke(client):
    response = await client.random()
    assert isinstance(response, Blague)


async def test_random_with_disallowed(client):
    response = await client.random(disallow=["dark"])
    assert isinstance(response, Blague)
    assert response.type != BlagueType.DARK


async def test_random_with_allowed(client):
    response = await client.random_categorized(BlagueType.DARK)
    assert isinstance(response, Blague)
    assert response.type == BlagueType.DARK


async def test_from_id(client):
    response = await client.from_id(1)
    assert isinstance(response, Blague)
    assert response.id == 1


async def test_count_joke(client):
    response = await client.count()
    assert isinstance(response, CountJoke)
