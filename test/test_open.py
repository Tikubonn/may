
from .test_server import TestServer
from unittest import TestCase
from may import open_may
from pathlib import Path

TESTDATA = "test text for test of file IO emulation."


class TestOpen (TestCase):

    def test_open(self):
        with TestServer():
            with open_may("localhost", user="test", passwd="passwd") as may:

                # write then read

                with may.open("example.txt", "w") as stream:
                    stream.write(TESTDATA)

                with may.open("example.txt", "r") as stream:
                    self.assertEqual(stream.read(), TESTDATA)

                # try read unexists file

                with self.assertRaises(FileNotFoundError):
                    with may.open("unexists-file.txt", "r"):
                        pass

                # try read directory

                may.mkdir("exampledir")

                with self.assertRaises(PermissionError):
                    with may.open("exampledir", "w"):
                        pass

                with self.assertRaises(PermissionError):
                    with may.open("exampledir", "r"):
                        pass
