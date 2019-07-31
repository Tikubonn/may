
# May 

![Python 3.6](https://img.shields.io/badge/Python-3.6-blue.svg "Python 3.6")
![MIT](https://img.shields.io/badge/License-MIT-green.svg "MIT")

May provide a FTP wrapper that can control the FTP like as file system. 
this library is useful than using FTP protocol directory, but applications performance will be wrong, because this trade the performance to abstraction. 

## Usage

first, import function of `open_may` from package, then call it for open the FTP connection and get a new instance.
this example, opened new FTP connection, then change directory and download all files in the directory.

```python3 
from may import open_may

may = open_may("localhost", user="tikubonn", passwd="passwd")
may.chdir("example")

for file in may.iterdir():
    if may.isfile(file):
        may.download(file, file.name) # download remote file to local.

may.close() # quit and close.
```

class has supported the with context, so you can write code like as this.

```python3 
with open_may("localhost", user="tikubonn", passwd="passwd") as may:
    pass
```

if you want to use SFTP, you can import `open_may_tls` for alternate of `open_may`.

```python3
from may import open_may_tls
```

## Installation

May has a [setup.py](setup.py) so you can install with this command.

```shell
$ python setup.py install
```

## License 

May has released under the [MIT License](LICENSE).
