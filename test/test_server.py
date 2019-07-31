
from tempfile import TemporaryDirectory
from pathlib import Path
import subprocess 
import sys 

class TestServer:
  
  """
  open the FTP server for unittest.
  """
  
  def __init__ (self, host="localhost", port=21, user="test", passwd="passwd"):
    self.host = host
    self.port = port
    self.user = user
    self.passwd = passwd
    self.process = None 
    self.tempdir = None 
    self.open() # open FTP server.
  
  def __enter__ (self):
    return self
  
  def __exit__ (self, error, errorvalue, backtrace):
    self.close()
  
  def open (self):
    
    """
    open the FTP server that manage the temporary directory.
    """
    
    self.tempdir = TemporaryDirectory()
    self.process = subprocess.Popen(
      args=(
        sys.executable,
        "-m", "pyftpdlib", 
        "-i", str(self.host),
        "-p", str(self.port),
        "-u", str(self.user),
        "-P", str(self.passwd),
        "-d", Path(self.tempdir.name).as_posix(),
        "-w"
      ),
      stdin=subprocess.DEVNULL,
      stdout=subprocess.DEVNULL,
      stderr=subprocess.DEVNULL
    )
  
  def close (self):
    
    """
    close the opened FTP server and cleanup temporary directory.
    """
    
    self.tempdir.cleanup()
    self.process.kill()
    self.process.wait()
