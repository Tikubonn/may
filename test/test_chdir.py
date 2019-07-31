
from .test_server import TestServer
from unittest import TestCase
from may import open_may
from pathlib import Path

TESTDATA = "test text for test of file IO emulation."


class TestChdir (TestCase):

    def test_chdir(self):
        with TestServer():
            with open_may("localhost", user="test", passwd="passwd") as may:

                # make directories

                may.makedirs("example1/example11", exist_ok=True)
                may.makedirs("example1/example12", exist_ok=True)
                may.makedirs("example1/example12/example121", exist_ok=True)

                # change dir and check

                may.chdir("example1")
                self.assertEqual(may.curdir(), Path("/example1"))

                may.chdir("example12")
                self.assertEqual(may.curdir(), Path("/example1/example12"))

                may.chdir("example121")
                self.assertEqual(may.curdir(), Path(
                    "/example1/example12/example121"))

                with self.assertRaises(FileNotFoundError):
                    may.chdir("unknown-directory")

                may.chdir("/")
                self.assertEqual(may.curdir(), Path("/"))
