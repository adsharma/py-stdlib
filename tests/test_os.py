import os
import tempfile

from stdlib import pathlib
from stdlib.os import (  # replace 'your_module' with the actual name of your module
    chdir,
    getcwd,
    listdir,
    mkdir,
    remove,
    rename,
    rmdir,
    walk,
)


def path_exists(path: pathlib.Path) -> bool:
    return path.exists()


def test_mkdir():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = pathlib.Path(tmpdir)
        path = tmpdir_path / "new_dir"
        mkdir(str(path))
        assert path_exists(path) == True


def test_rmdir():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = pathlib.Path(tmpdir)
        path = tmpdir_path / "new_dir"
        mkdir(str(path))
        rmdir(str(path))
        assert path_exists(path) == False


def test_remove():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = pathlib.Path(tmpdir)
        path = tmpdir_path / "new_file"
        with open(str(path), "w") as f:
            f.write("Hello, world!")
        remove(str(path))
        assert path_exists(path) == False


def test_rename():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = pathlib.Path(tmpdir)
        src_path = tmpdir_path / "src_file"
        dst_path = tmpdir_path / "dst_file"
        with open(str(src_path), "w") as f:
            f.write("Hello, world!")
        rename(str(src_path), str(dst_path))
        assert path_exists(dst_path) == True
        assert path_exists(src_path) == False


def test_listdir():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = pathlib.Path(tmpdir)
        path1 = tmpdir_path / "file1"
        path2 = tmpdir_path / "file2"
        with open(str(path1), "w") as f:
            f.write("Hello, world!")
        with open(str(path2), "w") as f:
            f.write("Goodbye, world!")
        files = listdir(str(tmpdir_path))
        assert len(files) == 2
        # Check if the filenames are in the list
        assert path1.name in {f.name for f in files}
        assert path2.name in {f.name for f in files}


def test_walk():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = pathlib.Path(tmpdir)
        path1 = tmpdir_path / "file1"
        path2 = tmpdir_path / "dir1" / "file2"
        path2.parent.mkdir()  # Create the parent directory
        with open(str(path1), "w") as f:
            f.write("Hello, world!")
        with open(str(path2), "w") as f:
            f.write("Goodbye, world!")
        for root, dirs, files in walk(str(tmpdir_path)):
            if root == tmpdir_path:
                assert len(files) == 1
                assert len(dirs) == 1
            elif root == tmpdir_path / "dir1":
                assert len(files) == 1
                assert len(dirs) == 0


def test_chdir():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = pathlib.Path(tmpdir)
        original_dir = getcwd()
        chdir(str(tmpdir_path))
        assert getcwd() == tmpdir_path
        chdir(str(original_dir))


def test_getcwd():
    assert getcwd() == pathlib.Path(os.getcwd())
