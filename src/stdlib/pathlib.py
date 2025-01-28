import ctypes
import os
from typing import List, Union

from stdlib._os_types import DIR, Stat, dirent, libc

# Define function prototypes
libc.opendir.argtypes = [ctypes.c_char_p]
libc.opendir.restype = ctypes.POINTER(DIR)

libc.readdir.argtypes = [ctypes.POINTER(DIR)]
libc.readdir.restype = ctypes.POINTER(dirent)

libc.closedir.argtypes = [ctypes.POINTER(DIR)]
libc.closedir.restype = ctypes.c_int

libc.mkdir.argtypes = [ctypes.c_char_p, ctypes.c_int]
libc.mkdir.restype = ctypes.c_int

libc.unlink.argtypes = [ctypes.c_char_p]
libc.unlink.restype = ctypes.c_int

libc.rmdir.argtypes = [ctypes.c_char_p]
libc.rmdir.restype = ctypes.c_int

# Constants for access()
F_OK = 0  # Check if file exists
R_OK = 4  # Check if file is readable
W_OK = 2  # Check if file is writable
X_OK = 1  # Check if file is executable

# Constants for file type checks
S_IFMT = 0o170000  # Bitmask for the file type bit field
S_IFREG = 0o100000  # Regular file
S_IFDIR = 0o040000  # Directory


def stat(path: str) -> Stat:
    stat_result = Stat()
    path_bytes = path.encode("utf-8")

    if libc.stat(path_bytes, ctypes.byref(stat_result)) != 0:
        raise OSError(f"stat failed for path: {path}")

    return stat_result


class Path:
    def __init__(self, path: Union[str, "Path"]):
        self.path = str(path)

    def __str__(self):
        return self.path

    def __truediv__(self, other: Union[str, "Path"]) -> "Path":
        """Join paths using the / operator."""
        # TODO: Handle other platforms
        return Path(f"{self.path}/{other}")

    def exists(self) -> bool:
        """Check if the path exists."""
        return libc.access(self.path.encode("utf-8"), F_OK) == 0

    def is_dir(self) -> bool:
        """Check if the path is a directory."""
        return stat(self.path).st_mode & S_IFMT == S_IFDIR

    def is_file(self) -> bool:
        """Check if the path is a file."""
        return stat(self.path).st_mode & S_IFMT == S_IFREG

    def mkdir(self, mode: int = 0o755, parents: bool = False, exist_ok: bool = False):
        """Create a directory at this path."""
        if parents:
            os.makedirs(self.path, mode=mode, exist_ok=exist_ok)
        else:
            if libc.mkdir(self.path.encode("utf-8"), mode) != 0:
                if not exist_ok or not self.exists():
                    raise OSError(f"Failed to create directory: {self.path}")

    def rmdir(self):
        """Remove a directory at this path."""
        if libc.rmdir(self.path.encode("utf-8")) != 0:
            raise OSError(f"Failed to remove directory: {self.path}")

    def unlink(self):
        """Remove a file at this path."""
        if libc.unlink(self.path.encode("utf-8")) != 0:
            raise OSError(f"Failed to remove file: {self.path}")

    def iterdir(self) -> List["Path"]:
        """Iterate over the contents of a directory."""
        dir_ptr = libc.opendir(self.path.encode("utf-8"))
        if not dir_ptr:
            raise OSError(f"Could not open directory: {self.path}")

        entries = []
        while True:
            entry_ptr = libc.readdir(dir_ptr)
            if not entry_ptr:
                break
            entry = entry_ptr.contents
            name = entry.d_name.decode("utf-8")
            if name not in (".", ".."):
                entries.append(Path(os.path.join(self.path, name)))

        libc.closedir(dir_ptr)
        return entries

    def glob(self, pattern: str) -> List["Path"]:
        """Find paths matching a glob pattern."""
        import fnmatch

        return [
            child for child in self.iterdir() if fnmatch.fnmatch(child.path, pattern)
        ]

    @property
    def parent(self) -> "Path":
        """Return the parent directory of this path."""
        return Path(os.path.dirname(self.path))

    @property
    def name(self) -> str:
        """Return the base name of this path."""
        return os.path.basename(self.path)


# Example usage
if __name__ == "__main__":
    # Create a Path object
    p = Path("/tmp/mydir")

    # Create a directory
    p.mkdir(parents=True, exist_ok=True)

    # Check if the directory exists
    print(f"Directory exists: {p.exists()}")

    # Create a file
    file_path = p / "test.txt"
    with open(file_path.path, "w") as f:
        f.write("Hello, world!")

    # List directory contents
    print("Directory contents:")
    for child in p.iterdir():
        print(child)

    # Remove the file
    file_path.unlink()

    # Remove the directory
    p.rmdir()
