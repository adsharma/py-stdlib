import pytest
from stdlib import random


# Test randint
def test_randint():
    # Test valid range
    for _ in range(100):
        result = random.randint(1, 10)
        assert 1 <= result <= 10

    # Test invalid range
    with pytest.raises(ValueError):
        random.randint(10, 1)


# Test uniform
def test_uniform():
    # Test valid range
    for _ in range(100):
        result = random.uniform(1.0, 10.0)
        assert 1.0 <= result <= 10.0

    # Test invalid range
    with pytest.raises(ValueError):
        random.uniform(10.0, 1.0)


# Test choice
def test_choice():
    seq = ["apple", "banana", "cherry"]
    for _ in range(100):
        result = random.choice(seq)
        assert result in seq

    # Test empty sequence
    with pytest.raises(IndexError):
        random.choice([])


# Test shuffle
def test_shuffle():
    seq = [1, 2, 3, 4, 5]
    original = seq.copy()
    random.shuffle(seq)

    # Ensure the shuffled list has the same elements
    assert sorted(seq) == sorted(original)

    # Ensure the list is actually shuffled (probabilistic test)
    assert seq != original


# Test sample
def test_sample():
    population = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    k = 3

    for _ in range(100):
        result = random.sample(population, k)
        assert len(result) == k
        assert all(item in population for item in result)
        assert len(set(result)) == k  # Ensure no duplicates

    # Test k larger than population
    with pytest.raises(ValueError):
        random.sample(population, 20)


# Run tests
if __name__ == "__main__":
    pytest.main()
