
from .test_server import TestServer
from unittest import TestCase
from may import open_may
from pathlib import Path

class TestRmtree (TestCase):
  
  def test_rmtree (self):
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
        
        may.rmtree("example1") # directory

        with self.assertRaises(NotADirectoryError): # file 
          may.rmtree("not-a-directory.txt")
        
        with self.assertRaises(FileNotFoundError): # unexists 
          may.rmtree("example2")
        
        # check structures 
        
        rootfiles = list(may.iterdir("/"))
        self.assertEqual(len(rootfiles), 1)
        self.assertIn(Path("/not-a-directory.txt"), rootfiles)
        