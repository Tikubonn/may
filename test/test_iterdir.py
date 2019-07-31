
from .test_server import TestServer
from unittest import TestCase
from may import open_may
from tempfile import NamedTemporaryFile
from pathlib import Path


class TestIterdir (TestCase):

    def test_iterdir(self):
        with TestServer():
            with open_may("localhost", user="test", passwd="passwd") as may:

                # upload files

                tempfile = NamedTemporaryFile(delete=False)
                tempfile.close()
                may.upload(tempfile.name, "example1.txt")
                may.upload(tempfile.name, "example2.txt")
                may.upload(tempfile.name, "example3.txt")

                # iter directory files

                files = list(may.iterdir())
                self.assertEqual(len(files), 3)
                self.assertIn(Path("/example1.txt"), files)
                self.assertIn(Path("/example2.txt"), files)
                self.assertIn(Path("/example3.txt"), files)
