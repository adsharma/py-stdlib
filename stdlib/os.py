import ctypes
import os  # for strerrno
from typing import Generator, List, Tuple

from stdlib import pathlib
from stdlib._os_types import libc

# Define the constants for permissions
S_IRWXU = 0o700
S_IRWXG = 0o070
S_IRWXO = 0o007


def mkdir(path: str, mode=S_IRWXU | S_IRWXG | S_IRWXO) -> int:
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


def rmdir(path: str) -> int:
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


def remove(path: str) -> int:
    """
    Remove a file.

    :param path: The path to the file to remove.
    :return: 0 on success, -1 on failure.
    """
    # Convert the path to bytes
    path_bytes = path.encode("utf-8")
    # Call the unlink function
    result = libc.unlink(path_bytes)
    # Check for errors
    if result == -1:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno))
    return result


def rename(src: str, dst: str) -> int:
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


def listdir(path: pathlib.Path) -> List[pathlib.Path]:
    """
    Return a list of files and directories in the given path.

    :param path: The path to the directory to list.
    :return: A list of files and directories.
    """
    # Convert the path to bytes
    path_bytes = str(path).encode("utf-8")
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
                entries.append(pathlib.Path(entry_name))
    finally:
        # Close the directory
        libc.closedir(dir_p)
    return entries


def walk(top: str) -> Generator[Tuple[str, List[str], List[str]], None, None]:
    """Recursively walk a directory tree using libc."""
    dirs = []
    files = []

    # List the directory contents
    for name in listdir(top):
        full_path = pathlib.Path(top) / name
        if full_path.is_dir():
            dirs.append(name)
        else:
            files.append(name)

    # Yield the current directory's results
    yield top, dirs, files

    # Recurse into subdirectories
    for dir_name in dirs:
        new_top = pathlib.Path(top) / dir_name
        yield from walk(new_top)


def chdir(path) -> None:
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


def getcwd() -> str:
    """
    Return the current working directory.

    :return: The current working directory.
    """
    # Create a buffer to store the current working directory
    buffer = ctypes.create_string_buffer(1024)
    # Call the getcwd function
    result = libc.getcwd(buffer, 1024)
    # Check for errors
    if not result:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno))
    # Return the current working directory
    return buffer.value.decode("utf-8")
