
from .io_emulator import IOEmulator
from pathlib import Path
from shutil import copyfileobj, SameFileError
from datetime import datetime
from itertools import chain
from ftplib import FTP, FTP_TLS, error_perm
import re

REMDTM = re.compile("213 (\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})")


def open_may(*args, **keyargs):
    """
    connect to FTP server then return new May instance.
    if you want to close connection, call the instance's method of `close`.
    """

    ftp = FTP(*args, **keyargs)
    return May(ftp, firstdir=Path("/"))


def open_may_tls(*args, **keyargs):
    """
    connect to FTP server with TLS then return new May instance.
    if you want to close connection, call the instance's method of `close`.
    """

    ftp = FTP_TLS(*args, **keyargs)
    ftp.prot_p()
    return May(ftp, firstdir=Path("/"))


class May:

    """
    a FTP wrapper that like as file system.
    """

    def __init__(self, ftp, firstdir=Path("/")):
        """
        initialize instance with arguments.
        ftp object's current directory must be root directory.
        firstdir will be first current directory in instance.
        """

        self.ftp = ftp
        self.currentdir = Path(firstdir)

    def __enter__(self):
        return self

    def __exit__(self, error, errorvalue, backtrace):
        self.close()

    def close(self):
        self.ftp.quit()
        self.ftp.close()

    def curdir(self):
        """
        return the current directory.
        """

        return self.currentdir

    def chdir(self, directory):
        """
        change the current directory.
        if new directory was not found, this raise `FileNotFoundError`.
        """

        if not self.isdir(directory):
            raise FileNotFoundError(
                "directory of %r was not found." % (directory,))
        self.currentdir = self.currentdir.joinpath(directory)

    def exists(self, path):
        """
        return a boolean that path is exists or not.
        """

        if Path(path) == Path("/"):
            return True
        try:
            realpath = self.curdir().joinpath(path)
            for filename in self.ftp.nlst(realpath.parent.as_posix()):
                if filename == realpath.name:
                    return True
            return False

        # unrecommend code, because it depend to internal procedure of library.
        # but check file recursively is very low performance.

        except error_perm as error:
            message, = error.args
            if message.startswith("550"):
                return False
            raise

    def isfile(self, path):
        """
        return a boolean that path is file or not.
        """

        if Path(path) == Path("/"):
            return False
        try:
            realpath = self.curdir().joinpath(path)
            for filename, fileinfo in self.ftp.mlsd(realpath.parent.as_posix()):
                if filename == realpath.name:
                    return fileinfo["type"] == "file"
            return False

        # unrecommend code, because it depend to internal procedure of library.
        # but check file recursively is very low performance.

        except error_perm as error:
            message, = error.args
            if message.startswith("550"):
                return False
            raise

    def isdir(self, path):
        """
        return a boolean that path is directory or not.
        """

        if Path(path) == Path("/"):
            return True
        try:
            realpath = self.curdir().joinpath(path)
            for filename, fileinfo in self.ftp.mlsd(realpath.parent.as_posix()):
                if filename == realpath.name:
                    return fileinfo["type"] == "dir"
            return False

        # unrecommend code, because it depend to internal procedure of library.
        # but check file recursively is very low performance.

        except error_perm as error:
            message, = error.args
            if message.startswith("550"):
                return False
            raise

    def open(self, path, mode="r", *optionals, **keyoptionals):
        """
        return an file-like object that simulate file IO of remote file.
        """

        return IOEmulator(
            path,
            self,
            mode=mode,
            *optionals,
            **keyoptionals)

    def iterdir(self, directory=Path("./")):
        """
        return a generator that yield full file path.
        if directory was not found, this raise `FileNotFoundError`.
        if directory is not a directory, this raise `NotADirectoryError`.
        """

        realpath = self.curdir().joinpath(directory)
        if not self.exists(realpath):
            raise FileNotFoundError("file of %r was not found." % (realpath,))
        if not self.isdir(realpath):
            raise NotADirectoryError("%r is not a directory." % (realpath,))
        for file in self.ftp.nlst(realpath.as_posix()):
            yield realpath.joinpath(file)

    def remove(self, file):
        """
        remove remote file.
        if file was not found, this raise `FileNotFoundError`.
        if file is a directory, this raise `IsADirectoryError`.
        """

        realpath = self.curdir().joinpath(file)
        if not self.exists(realpath):
            raise FileNotFoundError("file of %r was not found." % (realpath,))
        if self.isdir(realpath):
            raise IsADirectoryError(
                "%r is not a file. it is directory." % (realpath,))
        self.ftp.delete(realpath.as_posix())

    def rmdir(self, directory):
        """
        remove remote directory.
        if directory was not found, this raise `FileNotFoundError`.
        if directory is a file, this raise `NotADirectoryError`.
        """

        realpath = self.curdir().joinpath(directory)
        if not self.exists(realpath):
            raise FileNotFoundError("file of %r was not found." % (realpath,))
        if not self.isdir(realpath):
            raise NotADirectoryError("%r is not a directory." % (realpath,))
        self.ftp.rmd(realpath.as_posix())

    def removedirs(self, directory):
        """
        remove remote empty directory recursively.
        """

        files = list(self.iterdir(directory))
        if not files:
            self.rmdir(directory)
        else:
            for file in files:
                if self.isdir(file):
                    self.removedirs(file)
            files = list(self.iterdir(directory))
            if not files:
                self.rmdir(directory.as_posix())

    def rmtree(self, directory):
        """
        remove remote directory and files recursively.
        """

        for file in self.iterdir(directory):
            if self.isfile(file):
                self.remove(file)
            elif self.isdir(file):
                self.rmtree(file)
        self.rmdir(directory)

    def rename(self, filefrom, fileto):
        """
        rename remote file.
        if two file path are same, this raise `SameFileError`.
        if file was not found, this raise `FileNotFoundError`.
        """

        if filefrom != fileto:
            realfilefrom = self.curdir().joinpath(filefrom)
            realfileto = self.curdir().joinpath(fileto)
            if not self.exists(realfilefrom):
                return FileNotFoundError("file of %r was not found." % (realfilefrom,))
            self.ftp.rename(
                realfilefrom.as_posix(),
                realfileto.as_posix())
        else:
            raise SameFileError("%r and %r are same path." %
                                (filefrom, fileto))

    def copy(self, filefrom, fileto):
        """
        copy remote file.
        if two file path are same, this raise `SameFileError`.
        """

        if filefrom != fileto:
            with self.open(filefrom, "rb") as inputstream:
                with self.open(fileto, "wb") as outputstream:
                    copyfileobj(inputstream, outputstream)
        else:
            raise SameFileError("%r and %r are same path." %
                                (filefrom, fileto))

    def copytree(self, filefrom, fileto):
        """
        copy remote directory recursively.
        if two file path are same, this raise `SameFileError`.
        """

        if Path(filefrom) != Path(fileto):
            if not self.isdir(fileto):
                self.mkdir(fileto)
            for file in self.iterdir(filefrom):
                if self.isfile(file):
                    self.copy(
                        Path(filefrom).joinpath(file.name),
                        Path(fileto).joinpath(file.name))
                elif self.isdir(file):
                    self.copytree(
                        Path(filefrom).joinpath(file.name),
                        Path(fileto).joinpath(file.name))
        else:
            raise SameFileError("%r and %r are same path." %
                                (filefrom, fileto))

    def lastmod(self, path):
        """
        return a number that is last modified time of file as unix-time of GMT.
        if file was not found, this raise `FileNotFoundError`.
        if server response is unsupported format, this raise `Error`.
        """

        realpath = self.curdir().joinpath(path)
        if not self.exists(realpath):
            raise FileNotFoundError("file of %r was not found." % (realpath,))
        response = self.ftp.sendcmd("MDTM %s" % (realpath.as_posix(),))
        matched = REMDTM.match(response)
        if matched:
            year, month, day, hours, minutes, seconds = map(
                int, matched.groups())
            return datetime(year, month, day, hours, minutes, seconds).timestamp()
        else:
            raise Error("got an unsupported response of %r." % (response,))

    def mkdir(self, directory):
        """
        make directory to remote server.
        if directory was already exists, this raise `FileExistsError`.
        """

        realpath = self.curdir().joinpath(directory)
        if self.exists(realpath):
            raise FileExistsError("%r was already exists." % (realpath,))
        self.ftp.mkd(realpath.as_posix())

    def makedirs(self, directory, exist_ok=False):
        """
        make directory recursively to remote server.
        if directory was already exists and `exist_ok` is False, this raise `FileExistsError`.
        if path was already exists as not directory, this raise `NotADirectoryError`.
        """

        realdirectory = self.curdir().joinpath(directory)
        for dir in chain(reversed(Path(realdirectory).parents), (Path(realdirectory),)):
            if dir != Path("/"):  # ignore root directory!
                if self.isdir(dir):
                    if not exist_ok:
                        raise FileExistsError(
                            "%r was already exists." % (dir,))
                elif self.exists(dir):
                    raise NotADirectoryError(
                        "%r was already exists, and it is not a directory." % (dir,))
                else:
                    self.mkdir(dir)

    def upload(self, srcpath, distpath, blocksize=8192):
        """
        upload local file to remote server.
        argument of `srcpath` must be local file path.
        argument of `distpath` must be remote file path.
        argument of `blocksize` must be larger than 0.
        """

        with open(srcpath, "rb") as inputstream:
            realpath = self.curdir().joinpath(distpath)
            self.ftp.storbinary("STOR %s" % (
                realpath.as_posix(),), inputstream, blocksize=blocksize)

    def download(self, srcpath, distpath, blocksize=8192):
        """
        download remote file to local file.
        argument of `srcpath` must be remote file path.
        argument of `distpath` must be local file path.
        argument of `blocksize` must be larger than 0.
        """

        with open(distpath, "wb") as outputstream:
            realpath = self.curdir().joinpath(srcpath)
            self.ftp.retrbinary("RETR %s" % (
                realpath.as_posix(),), outputstream.write, blocksize=blocksize)
