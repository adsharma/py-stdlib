import ctypes
import platform

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
    dirent = mac_dirent  # type: ignore # noqa: F811


class Stat(ctypes.Structure):
    _fields_ = [
        ("st_dev", ctypes.c_ulonglong),  # Device ID of the file
        ("st_ino", ctypes.c_ulonglong),  # Inode number
        ("st_nlink", ctypes.c_ulonglong),  # Number of hard links
        ("st_mode", ctypes.c_uint),  # File type and mode
        ("st_uid", ctypes.c_uint),  # User ID of the file's owner
        ("st_gid", ctypes.c_uint),  # Group ID of the file's owner
        ("st_rdev", ctypes.c_ulonglong),  # Device ID (if special file)
        ("st_size", ctypes.c_longlong),  # Total size in bytes
        ("st_blksize", ctypes.c_long),  # Optimal block size for I/O
        ("st_blocks", ctypes.c_longlong),  # Number of 512-byte blocks allocated
        ("st_atime", ctypes.c_long),  # Time of last access
        ("st_atime_nsec", ctypes.c_long),  # Nanoseconds of last access
        ("st_mtime", ctypes.c_long),  # Time of last modification
        ("st_mtime_nsec", ctypes.c_long),  # Nanoseconds of last modification
        ("st_ctime", ctypes.c_long),  # Time of last status change
        ("st_ctime_nsec", ctypes.c_long),  # Nanoseconds of last status change
    ]


class MacOSStat(ctypes.Structure):
    _fields_ = [
        ("st_dev", ctypes.c_uint32),  # Device ID of the file
        ("st_mode", ctypes.c_uint16),  # File type and mode
        ("st_nlink", ctypes.c_uint16),  # Number of hard links
        ("st_ino", ctypes.c_uint64),  # Inode number
        ("st_uid", ctypes.c_uint32),  # User ID of the file's owner
        ("st_gid", ctypes.c_uint32),  # Group ID of the file's owner
        ("st_rdev", ctypes.c_uint32),  # Device ID (if special file)
        ("st_atime", ctypes.c_long),  # Time of last access
        ("st_atimensec", ctypes.c_long),  # Nanoseconds of last access
        ("st_mtime", ctypes.c_long),  # Time of last modification
        ("st_mtimensec", ctypes.c_long),  # Nanoseconds of last modification
        ("st_ctime", ctypes.c_long),  # Time of last status change
        ("st_ctimensec", ctypes.c_long),  # Nanoseconds of last status change
        ("st_birthtime", ctypes.c_long),  # Time of file creation (birth)
        ("st_birthtimensec", ctypes.c_long),  # Nanoseconds of file creation
        ("st_size", ctypes.c_int64),  # Total size in bytes
        ("st_blocks", ctypes.c_int64),  # Number of 512-byte blocks allocated
        ("st_blksize", ctypes.c_int32),  # Optimal block size for I/O
        ("st_flags", ctypes.c_uint32),  # User-defined flags
        ("st_gen", ctypes.c_uint32),  # File generation number
        ("st_lspare", ctypes.c_int32),  # Reserved
        ("st_qspare", ctypes.c_int64 * 2),  # Reserved
    ]


if platform.system() == "Darwin":  # macOS
    Stat = MacOSStat  # type: ignore # noqa: F811

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

access = libc.access
access.argtypes = [ctypes.c_char_p, ctypes.c_int]
access.restype = ctypes.c_int

# Define the stat function
libc.stat.argtypes = [ctypes.c_char_p, ctypes.POINTER(Stat)]
libc.stat.restype = ctypes.c_int
