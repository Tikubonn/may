
from .test_server import TestServer
from unittest import TestCase
from may import open_may
from pathlib import Path
from shutil import SameFileError

TESTDATA = "this is a test text."


class TestCopytree (TestCase):

    def test_copytree(self):
        with TestServer():
            with open_may("localhost", user="test", passwd="passwd") as may:

                # make directory and files
                #
                # keep.txt
                # example1 =>
                #   keep.txt
                #   example11 =>
                #     keep1.txt
                #     keep2.txt
                #   example12 =>

                may.makedirs("example1", exist_ok=True)
                may.makedirs("example1/example11", exist_ok=True)
                may.makedirs("example1/example12", exist_ok=True)

                with may.open("keep.txt", "w"):
                    pass

                with may.open("example1/keep.txt", "w"):
                    pass

                with may.open("example1/example11/keep1.txt", "w"):
                    pass

                with may.open("example1/example11/keep2.txt", "w"):
                    pass

                # copy directory

                may.copytree("example1", "example2")

                # with self.assertRaises(NotADirectoryError):
                #   may.copytree("keep.txt", "keep2.txt")

                with self.assertRaises(SameFileError):
                    may.copytree("example1", "example1")

                # check directories

                rootfiles = list(may.iterdir("/"))
                self.assertEqual(len(rootfiles), 3)
                self.assertIn(Path("/keep.txt"), rootfiles)
                self.assertIn(Path("/example1"), rootfiles)
                self.assertIn(Path("/example2"), rootfiles)

                example2files = list(may.iterdir("/example2"))
                self.assertEqual(len(example2files), 3)
                self.assertIn(Path("/example2/keep.txt"), example2files)
                self.assertIn(Path("/example2/example11"), example2files)
                self.assertIn(Path("/example2/example12"), example2files)

                example11files = list(may.iterdir("/example2/example11"))
                self.assertEqual(len(example11files), 2)
                self.assertIn(
                    Path("/example2/example11/keep1.txt"), example11files)
                self.assertIn(
                    Path("/example2/example11/keep2.txt"), example11files)

                example12files = list(may.iterdir("/example2/example12"))
                self.assertEqual(len(example12files), 0)
