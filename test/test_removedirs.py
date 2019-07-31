
from .test_server import TestServer
from unittest import TestCase
from may import open_may
from pathlib import Path

class TestRemovedirs (TestCase):
  
  def test_removedirs (self):
    with TestServer():
      with open_may("localhost", user="test", passwd="passwd") as may:
        
        # make directories and files 
        #
        # not-a-directory.txt
        # example1 =>
        #   example11 => 
        #     example111 
        #     example112 
        #   example12 => 
        #     keep.txt
        #   example13 
        
        may.makedirs("example1/example11", exist_ok=True)
        may.makedirs("example1/example11/example111", exist_ok=True)
        may.makedirs("example1/example11/example112", exist_ok=True)
        may.makedirs("example1/example12", exist_ok=True)
        may.makedirs("example1/example13", exist_ok=True)
        
        with may.open("not-a-directory.txt", "w"):
          pass
        
        with may.open("example1/example12/keep.txt", "w"):
          pass
        
        # remove directories 
        
        may.removedirs("example1") # directory

        with self.assertRaises(NotADirectoryError): # file 
          may.removedirs("not-a-directory.txt")
        
        with self.assertRaises(FileNotFoundError): # unexists 
          may.removedirs("example2")
        
        # check structures 
        
        rootfiles = list(may.iterdir("/"))
        self.assertEqual(len(rootfiles), 2)
        self.assertIn(Path("/not-a-directory.txt"), rootfiles)
        self.assertIn(Path("/example1"), rootfiles)
        
        example1files = list(may.iterdir("/example1"))
        self.assertEqual(len(example1files), 1)
        self.assertIn(Path("/example1/example12"), example1files)
        
        example12files = list(may.iterdir("/example1/example12"))
        self.assertEqual(len(example12files), 1)
        self.assertIn(Path("/example1/example12/keep.txt"), example12files)
        