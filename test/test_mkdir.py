
from .test_server import TestServer
from unittest import TestCase
from may import open_may
from pathlib import Path

class TestMkdir (TestCase):
  
  def test_mkdir (self):
    with TestServer():
      with open_may("localhost", user="test", passwd="passwd") as may:
        
        # make directory
        
        may.mkdir("example1")
        may.mkdir("example2")
        may.mkdir("example2/example21")
        may.mkdir("example2/example22")
        
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
        