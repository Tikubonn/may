
from .test_server import TestServer
from unittest import TestCase
from tempfile import NamedTemporaryFile
from pathlib import Path
from may import open_may

TESTDATA = "test text."

class TestUploadAndDownload (TestCase):
  
  def test_upload_and_download (self):
    with TestServer():
      with open_may("localhost", user="test", passwd="passwd") as may:
        
        # upload 
        
        tempfileup = NamedTemporaryFile(mode="w", encoding="utf-8", delete=False)
        tempfileup.write(TESTDATA)
        tempfileup.close()
        may.upload(
          tempfileup.name,
          Path(tempfileup.name).name)
        
        # download 
        
        tempfiledown = NamedTemporaryFile(delete=False)
        tempfiledown.close()
        may.download(
          Path(tempfileup.name).name,
          tempfiledown.name)
        with open(tempfiledown.name, "r") as stream:
          self.assertEqual(TESTDATA, stream.read())
