
from .test_server import TestServer
from unittest import TestCase
from may import open_may
from pathlib import Path


class TestExists (TestCase):

    def test_exists(self):
        with TestServer():
            with open_may("localhost", user="test", passwd="passwd") as may:

                # make directory

                may.mkdir("exampledir")

                # open file then write

                with may.open("example.txt", "w") as stream:
                    pass

                self.assertTrue(may.exists("example.txt"))  # file
                self.assertTrue(may.exists("exampledir"))  # directory
                self.assertFalse(may.exists("example1.txt"))  # not exists
