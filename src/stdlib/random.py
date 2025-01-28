import ctypes
import time
from typing import Any, List, Sequence, TypeVar

T = TypeVar("T")

# Load the libc library
libc = ctypes.CDLL(None)

try:
    RAND_MAX = ctypes.c_int.in_dll(libc, "RAND_MAX").value
except ValueError:
    # RAND_MAX is typically 2^31 - 1 on most systems
    RAND_MAX = 2147483647  # Maximum value for libc.rand() on most systems

    print(f"Guessed RAND_MAX = {RAND_MAX}")

# Define the rand() and srand() functions from libc
libc.rand.argtypes = []
libc.rand.restype = ctypes.c_int

libc.srand.argtypes = [ctypes.c_uint]
libc.srand.restype = None

# Seed the random number generator with the current time
libc.srand(int(time.time()))


def randint(a: int, b: int) -> int:
    """Return a random integer N such that a <= N <= b."""
    if a > b:
        raise ValueError("a must be less than or equal to b")
    return a + (libc.rand() % (b - a + 1))


def uniform(a: float, b: float) -> float:
    """Return a random float N such that a <= N <= b."""
    if a > b:
        raise ValueError("a must be less than or equal to b")

    # Generate a random float in [0, 1]
    random_float = libc.rand() / RAND_MAX

    # Scale to [a, b]
    return a + random_float * (b - a)


def choice(seq: Sequence[T]) -> T:
    """Return a random element from a non-empty sequence."""
    if not seq:
        raise IndexError("Cannot choose from an empty sequence")
    index = randint(0, len(seq) - 1)
    return seq[index]


def shuffle(seq: List[Any]) -> None:
    """Shuffle a list in place using the Fisher-Yates algorithm."""
    for i in range(len(seq) - 1, 0, -1):
        j = randint(0, i)
        seq[i], seq[j] = seq[j], seq[i]


def sample(population: Sequence[T], k: int) -> List[T]:
    """Return a list of k unique elements randomly chosen from the population."""
    if k > len(population):
        raise ValueError("k cannot be greater than the population size")
    shuffled = list(population)
    shuffle(shuffled)
    return shuffled[:k]
