
from .test_server import TestServer
from unittest import TestCase
from may import open_may
from pathlib import Path


class TestIsDir (TestCase):

    def test_isdir(self):
        with TestServer():
            with open_may("localhost", user="test", passwd="passwd") as may:

                # make directory

                may.mkdir("exampledir")

                # open file then write

                with may.open("example.txt", "w") as stream:
                    pass

                self.assertTrue(may.isdir("exampledir"))  # directory
                self.assertFalse(may.isdir("example.txt"))  # file
                self.assertFalse(may.isdir("example1.txt"))  # not exists
