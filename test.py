import asyncio

import os
from unittest import TestCase
from dotenv import dotenv_values
from blagues_api import BlaguesAPI, BlagueType, Blague

config = dotenv_values(".env")

blagues = BlaguesAPI(config.token)

class WrapperTests(TestCase):

    def test_token(self):
        """ Check token existance in .env """
        self.assertIsInstance(config.token, str)

    def test_random_joke(self):
        """ Check random joke """
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(blagues.random())
        self.assertIsInstance(response, Blague)

    def test_random_with_disallowed(self):
        """ Check random with disallowed DARK type """
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(blagues.random(disallow=["dark"]))
        self.assertIsInstance(response, Blague)
        self.assertNotEqual(response.type, BlagueType.DARK)

    def test_random_with_allowed(self):
        """ Check random with disallowed DARK type """
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(blagues.random_categorized(category=BlagueType.DARK))
        self.assertIsInstance(response, Blague)
        self.assertEqual(response.type, BlagueType.DARK)
    
    def test_by_id(self):
        """ Check random with disallowed DARK type """
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(blagues.from_id(1))
        self.assertIsInstance(response, Blague)
        self.assertEqual(response.id, 1)

if __name__ == '__main__':
    unittest.main()
