import ctypes
import os
import platform
from typing import Generator, Tuple, List


# Load the libc library
libc = ctypes.CDLL(None)


# Define the necessary types and structures
class DIR(ctypes.Structure):
    pass


class dirent(ctypes.Structure):
    _fields_ = [
        ("d_ino", ctypes.c_ulong),
        ("d_off", ctypes.c_long),
        ("d_reclen", ctypes.c_ushort),
        ("d_type", ctypes.c_ubyte),
        ("d_name", ctypes.c_char * 256),
    ]


class mac_dirent(ctypes.Structure):
    _fields_ = [
        ("d_fileno", ctypes.c_ulong),  # ino_t (file number of entry)
        ("d_seekoff", ctypes.c_uint64),  # __uint64_t (seek offset)
        ("d_reclen", ctypes.c_uint16),  # __uint16_t (length of this record)
        ("d_namlen", ctypes.c_uint16),  # __uint16_t (length of string in d_name)
        ("d_type", ctypes.c_uint8),  # __uint8_t (file type)
        ("d_name", ctypes.c_char * 1024),  # char[1024] (name of the entry)
    ]


if platform.system() == "Darwin":  # macOS
    dirent = mac_dirent  # noqa: F811

# Define the function prototypes
libc.opendir.argtypes = [ctypes.c_char_p]
libc.opendir.restype = ctypes.POINTER(DIR)

libc.readdir.argtypes = [ctypes.POINTER(DIR)]
libc.readdir.restype = ctypes.POINTER(dirent)

libc.closedir.argtypes = [ctypes.POINTER(DIR)]
libc.closedir.restype = ctypes.c_int

# Define the mkdir function prototype
mkdir = libc.mkdir
mkdir.argtypes = [ctypes.c_char_p, ctypes.c_int]
mkdir.restype = ctypes.c_int

# Define the rmdir function prototype
rmdir = libc.rmdir
rmdir.argtypes = [ctypes.c_char_p]
rmdir.restype = ctypes.c_int

# Define the unlink function prototype (for remove)
unlink = libc.unlink
unlink.argtypes = [ctypes.c_char_p]
unlink.restype = ctypes.c_int

# Define the rename function prototype
rename = libc.rename
rename.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
rename.restype = ctypes.c_int

# Define the chdir function prototype
chdir = libc.chdir
chdir.argtypes = [ctypes.c_char_p]
chdir.restype = ctypes.c_int

# Define the getcwd function prototype
getcwd = libc.getcwd
getcwd.argtypes = [ctypes.c_char_p, ctypes.c_size_t]
getcwd.restype = ctypes.c_char_p

# Define the closedir function prototype (for listdir)
closedir = libc.closedir
closedir.argtypes = [ctypes.c_void_p]
closedir.restype = ctypes.c_int

# Define the constants for permissions
S_IRWXU = 0o700
S_IRWXG = 0o070
S_IRWXO = 0o007


def path_join(*paths):
    """
    Join multiple path components together.

    :param paths: The path components to join.
    :return: The joined path.
    """
    return "/".join(paths)


def path_exists(path):
    """
    Check if a path exists.

    :param path: The path to check.
    :return: True if the path exists, False otherwise.
    """
    # Use the access function to check if the path exists
    access = libc.access
    access.argtypes = [ctypes.c_char_p, ctypes.c_int]
    access.restype = ctypes.c_int
    return access(path.encode("utf-8"), 0) == 0


def mkdir(path, mode=S_IRWXU | S_IRWXG | S_IRWXO):
    """
    Create a directory.

    :param path: The path to the directory to create.
    :param mode: The permissions to use for the new directory.
    :return: 0 on success, -1 on failure.
    """
    # Convert the path to bytes
    path_bytes = path.encode("utf-8")
    # Call the mkdir function
    result = libc.mkdir(path_bytes, mode)
    # Check for errors
    if result == -1:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno))
    return result


def rmdir(path):
    """
    Remove a directory.

    :param path: The path to the directory to remove.
    :return: 0 on success, -1 on failure.
    """
    # Convert the path to bytes
    path_bytes = path.encode("utf-8")
    # Call the rmdir function
    result = libc.rmdir(path_bytes)
    # Check for errors
    if result == -1:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno))
    return result


def remove(path):
    """
    Remove a file.

    :param path: The path to the file to remove.
    :return: 0 on success, -1 on failure.
    """
    # Convert the path to bytes
    path_bytes = path.encode("utf-8")
    # Call the unlink function
    result = unlink(path_bytes)
    # Check for errors
    if result == -1:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno))
    return result


def rename(src, dst):
    """
    Rename a file or directory.

    :param src: The source path.
    :param dst: The destination path.
    :return: 0 on success, -1 on failure.
    """
    # Convert the paths to bytes
    src_bytes = src.encode("utf-8")
    dst_bytes = dst.encode("utf-8")
    # Call the rename function
    result = libc.rename(src_bytes, dst_bytes)
    # Check for errors
    if result == -1:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno))
    return result


def listdir(path):
    """
    Return a list of files and directories in the given path.

    :param path: The path to the directory to list.
    :return: A list of files and directories.
    """
    # Convert the path to bytes
    path_bytes = path.encode("utf-8")
    # Open the directory
    dir_p = libc.opendir(path_bytes)
    if dir_p is None:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno))
    try:
        # Read the directory entries
        entries = []
        while True:
            entry_p = libc.readdir(dir_p)
            if not entry_p:
                break
            entry = entry_p.contents
            entry_name = entry.d_name.decode("utf-8")
            if entry_name != "." and entry_name != "..":
                entries.append(entry_name)
    finally:
        # Close the directory
        closedir(dir_p)
    return entries


def walk(top: str) -> Generator[Tuple[str, List[str], List[str]], None, None]:
    """Recursively walk a directory tree using libc."""
    dirs = []
    files = []

    # List the directory contents
    for name in listdir(top):
        full_path = os.path.join(top, name)
        if os.path.isdir(full_path):
            dirs.append(name)
        else:
            files.append(name)

    # Yield the current directory's results
    yield top, dirs, files

    # Recurse into subdirectories
    for dir_name in dirs:
        new_top = os.path.join(top, dir_name)
        yield from walk(new_top)


def chdir(path):
    """
    Change the current working directory.

    :param path: The path to the new current working directory.
    :return: None
    """
    # Convert the path to bytes
    path_bytes = path.encode("utf-8")
    # Call the chdir function
    result = libc.chdir(path_bytes)
    # Check for errors
    if result == -1:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno))


def getcwd():
    """
    Return the current working directory.

    :return: The current working directory.
    """
    # Create a buffer to store the current working directory
    buffer = ctypes.create_string_buffer(1024)
    # Call the getcwd function
    result = libc.getcwd(buffer, 1024)
    # Check for errors
    if result is None:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno))
    # Return the current working directory
    return buffer.value.decode("utf-8")
