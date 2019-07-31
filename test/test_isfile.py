
from .test_server import TestServer
from unittest import TestCase
from may import open_may
from pathlib import Path

class TestIsFile (TestCase):
  
  def test_isfile (self):
    with TestServer():
      with open_may("localhost", user="test", passwd="passwd") as may:
        
        # make directory

        may.mkdir("exampledir")
        
        # open file then write
        
        with may.open("example.txt", "w") as stream:
          pass
                
        self.assertTrue(may.isfile("example.txt")) # file 
        self.assertFalse(may.isfile("example1.txt")) # not exists 
        self.assertFalse(may.isfile("exampledir")) # directory 
        