
from .test_server import TestServer
from unittest import TestCase
from may import open_may
from pathlib import Path


class TestMakedirs (TestCase):

    def test_makedirs(self):
        with TestServer():
            with open_may("localhost", user="test", passwd="passwd") as may:

                # make directory

                may.makedirs("example1", exist_ok=True)
                may.makedirs("example2/example21", exist_ok=True)
                may.makedirs("example2/example22", exist_ok=True)

                # try make directory (always raise error)

                with self.assertRaises(FileExistsError):
                    may.makedirs("example1", exist_ok=False)
                with self.assertRaises(FileExistsError):
                    may.makedirs("example2/example21", exist_ok=False)
                with self.assertRaises(FileExistsError):
                    may.makedirs("example2/example22", exist_ok=False)

                # check directory

                rootfiles = list(may.iterdir(""))
                self.assertEqual(len(rootfiles), 2)
                self.assertIn(Path("/example1"), rootfiles)
                self.assertIn(Path("/example2"), rootfiles)

                example1files = list(may.iterdir("example1"))
                self.assertEqual(len(example1files), 0)

                example2files = list(may.iterdir("example2"))
                self.assertEqual(len(example2files), 2)
                self.assertIn(Path("/example2/example21"), example2files)
                self.assertIn(Path("/example2/example22"), example2files)
