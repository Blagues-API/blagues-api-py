import asyncio
import unittest
import os
import dotenv

from blagues_api import BlaguesAPI, BlagueType, Blague

dotenv.load_dotenv()

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMzI0OTQxNDcyMzY3NjQwNTk2IiwibGltaXQiOjEwMCwia2V5IjoiOHJ2QVdPaEhzdHJlNFRPMFA0MXNZRlMzZTVuajA3QnJOOER2eUwyVFhvczRWUGZ0a0UiLCJjcmVhdGVkX2F0IjoiMjAyMS0wNi0wOVQxNzoyMzozMiswMDowMCIsImlhdCI6MTYyMzI1OTQxMn0.QyqzFGEigCz0yd0K_HJkk8lIABrpI9UDf3UVfSkDIsc" #os.getenv('MY_ENV_VAR')

blagues = BlaguesAPI(TOKEN)

class WrapperTests(unittest.TestCase):

    def test_token(self):
        """ Check token existance in .env """
        self.assertIsInstance(TOKEN, str)
    
    def test_random_joke(self):
        """ Check random joke """
        loop = asyncio.get_event_loop()
        reponce = loop.run_until_complete(blagues.random())
        self.assertIsInstance(reponce, Blague)
        self.assertIsInstance(reponce.id, int)
        self.assertIn(reponce.type, BlagueType)
        self.assertIsInstance(reponce.joke, str)
        self.assertIsInstance(reponce.answer, str)

    def test_random_with_disallowed(self):
        """ Check random with disallowed DARK type """
        loop = asyncio.get_event_loop()
        reponce = loop.run_until_complete(blagues.random(disallow=["dark"]))
        self.assertIsInstance(reponce, Blague)
        self.assertIsInstance(reponce.id, int)
        self.assertNotEqual(reponce.type, BlagueType.DARK)
        self.assertIsInstance(reponce.joke, str)
        self.assertIsInstance(reponce.answer, str)

    def test_random_with_allowed(self):
        """ Check random with disallowed DARK type """
        loop = asyncio.get_event_loop()
        reponce = loop.run_until_complete(blagues.random_categorized(disallow=["dark"]))
        self.assertIsInstance(reponce, Blague)
        self.assertIsInstance(reponce.id, int)
        self.assertEqual(reponce.type, BlagueType.DARK)
        self.assertIsInstance(reponce.joke, str)
        self.assertIsInstance(reponce.answer, str)
    
    def test_by_id(self):
        """ Check random with disallowed DARK type """
        loop = asyncio.get_event_loop()
        reponce = loop.run_until_complete(blagues.from_id(1))
        self.assertIsInstance(reponce, Blague)
        self.assertEqual(reponce.id, 1)
        self.assertEqual(reponce.type, BlagueType)
        self.assertIsInstance(reponce.joke, str)
        self.assertIsInstance(reponce.answer, str)


if __name__ == '__main__':
    unittest.main()
