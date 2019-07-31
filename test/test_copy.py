
from .test_server import TestServer
from unittest import TestCase
from may import open_may
from pathlib import Path
from shutil import SameFileError

TESTDATA = "this is a test text."


class TestCopy (TestCase):

    def test_copy(self):
        with TestServer():
            with open_may("localhost", user="test", passwd="passwd") as may:

                # create directory and file

                may.mkdir("exampledir")

                with may.open("example.txt", "w") as stream:
                    stream.write(TESTDATA)

                # copy file

                may.copy("example.txt", "example2.txt")

                with self.assertRaises(PermissionError):
                    may.copy("exampledir", "exampledir2")

                with self.assertRaises(FileNotFoundError):
                    may.copy("unexists-file.txt", "unexists-file2.txt")

                with self.assertRaises(SameFileError):
                    may.copy("example.txt", "example.txt")

                # check the content

                with may.open("example.txt", "r") as stream:
                    self.assertEqual(TESTDATA, stream.read())
