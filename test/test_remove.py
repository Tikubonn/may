
from .test_server import TestServer
from unittest import TestCase
from may import open_may
from pathlib import Path

class TestRemove (TestCase):
  
  def test_remove (self):
    with TestServer():
      with open_may("localhost", user="test", passwd="passwd") as may:
        
        # make directory 
        
        may.mkdir("exampledir")
        
        # open file then write
        
        with may.open("example.txt", "w") as stream:
          pass
        
        # try remove file, directory and unexists file 
        
        may.remove("example.txt") # file 
        
        with self.assertRaises(IsADirectoryError): # directory 
          may.remove("exampledir")
        
        with self.assertRaises(FileNotFoundError): # unexists  
          may.remove("example1.txt")

        # check removed file 
        
        files = list(may.iterdir())
        self.assertEqual(len(files), 1)
        self.assertIn(Path("/exampledir"), files)
