import pytest

from dotenv import dotenv_values
import os, platform
import asyncio
try:
    from blagues_api import BlaguesAPI, Blague, BlagueType
except ImportError:
    try:
        if platform.system().lower().startswith('win'):
            os.system("pip install blagues-api")
        else:
            os.system("pip3 install blagues-api")
    except Exception as e:
        print("Package Installation Error:", e)
        exit()

pytestmark = pytest.mark.asyncio


@pytest.fixture
def token():
    env = dotenv_values(".env")
    return env["TOKEN"]


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
