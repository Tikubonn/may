
from io import IOBase
from tempfile import NamedTemporaryFile


class IOEmulator (IOBase):

    """
    this class emulate file IO for remote file.
    it will download or upload the content to remote server if necessary.
    """

    def __init__(self, remotepath, may, mode="r", *optionals, **keyoptionals):
        """
        initialize the instance.
        argument of `mode`, `encoding`, `optionals` and `keyoptionals` are used to 
        call the internal function of `open_template`.
        """

        self.remotepath = remotepath
        self.may = may
        self.tempfile = self.open_tempfile(
            mode=mode,
            *optionals,
            **keyoptionals)

    # private
    def get_tempname(self):
        with NamedTemporaryFile(delete=False) as tempfile:
            return tempfile.name

    # private
    def open_tempfile(self, mode="r", *optionals, **keyoptionals):
        # directory is not a file in this library xD
        if self.may.isdir(self.remotepath):
            raise PermissionError(
                "could not open the directory %r like as file." % (self.remotepath,))
        tempname = self.get_tempname()
        if "r" in mode:
            # file must be exists on read mode xD
            if not self.may.exists(self.remotepath):
                raise FileNotFoundError(
                    "file %r was not found." % (self.remotepath,))
            self.may.download(self.remotepath, tempname)
        elif "+" in mode:
            if self.may.exists(self.remotepath):
                self.may.download(self.remotepath, tempname)
        return open(
            tempname,
            mode=mode,
            *optionals,
            **keyoptionals)

    # override
    def close(self):
        """
        close this object.
        if this open mode has "w" or "a", upload the temporary file to remote server.
        """

        self.tempfile.close()
        if ("w" in self.tempfile.mode or
                "a" in self.tempfile.mode):
            self.may.upload(self.tempfile.name, self.remotepath)

    # private
    def fileno(self, *args, **keyargs):
        """
        call the internal file object's  method of `fileno` with arguments.
        """

        return self.tempfile.fileno(*args, **keyargs)

    # private
    def flush(self, *args, **keyargs):
        """
        call the internal file object's  method of `flush` with arguments.
        """

        return self.tempfile.flush(*args, **keyargs)

    # private
    def isatty(self, *args, **keyargs):
        """
        call the internal file object's  method of `isatty` with arguments.
        """

        return self.tempfile.isatty(*args, **keyargs)

    # private
    def readable(self, *args, **keyargs):
        """
        call the internal file object's  method of `readable` with arguments.
        """

        return self.tempfile.readable(*args, **keyargs)

    # private
    def readline(self, *args, **keyargs):
        """
        call the internal file object's  method of `readline` with arguments.
        """

        return self.tempfile.readline(*args, **keyargs)

    # private
    def readlines(self, *args, **keyargs):
        """
        call the internal file object's  method of `readlines` with arguments.
        """

        return self.tempfile.readlines(*args, **keyargs)

    # private
    def read(self, *args, **keyargs):
        """
        call the internal file object's  method of `read` with arguments.
        """

        return self.tempfile.read(*args, **keyargs)

    # private
    def seek(self, *args, **keyargs):
        """
        call the internal file object's  method of `seek` with arguments.
        """

        return self.tempfile.seek(*args, **keyargs)

    # private
    def seekable(self, *args, **keyargs):
        """
        call the internal file object's  method of `seekable` with arguments.
        """

        return self.tempfile.seekable(*args, **keyargs)

    # private
    def tell(self, *args, **keyargs):
        """
        call the internal file object's  method of `tell` with arguments.
        """

        return self.tempfile.tell(*args, **keyargs)

    # private
    def truncate(self, *args, **keyargs):
        """
        call the internal file object's  method of `truncate` with arguments.
        """

        return self.tempfile.truncate(*args, **keyargs)

    # private
    def writable(self, *args, **keyargs):
        """
        call the internal file object's  method of `writable` with arguments.
        """

        return self.tempfile.writable(*args, **keyargs)

    # private
    def writelines(self, *args, **keyargs):
        """
        call the internal file object's  method of `writelines` with arguments.
        """

        return self.tempfile.writelines(*args, **keyargs)

    # private
    def write(self, *args, **keyargs):
        """
        call the internal file object's  method of `write` with arguments.
        """

        return self.tempfile.write(*args, **keyargs)
