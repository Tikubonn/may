
from .test_server import TestServer
from unittest import TestCase
from may import open_may
from pathlib import Path
from shutil import SameFileError

class TestRename (TestCase):
  
  def test_rename (self):
    with TestServer():
      with open_may("localhost", user="test", passwd="passwd") as may:
        
        # make directory and file 
        
        may.mkdir("exampledir")
        
        with may.open("example.txt", "w"):
          pass
        
        # rename files 
        
        may.rename("exampledir", "exampledir2")
        may.rename("example.txt", "example2.txt")
        
        with self.assertRaises(SameFileError):
          may.rename("exampledir", "exampledir")
        
        with self.assertRaises(SameFileError):
          may.rename("example.txt", "example.txt")
        
        # check the structure
        
        files = list(may.iterdir())
        self.assertEqual(len(files), 2)
        self.assertIn(Path("/exampledir2"), files)
        self.assertIn(Path("/example2.txt"), files)
