from stdlib._cffi_util import load_library

# Load the shared library
lib = load_library("regex_wrapper")


def match(pattern: str, text: str) -> bool:
    return lib.match(
        pattern.encode("utf-8"), text.encode("utf-8")
    )  # pyright: ignore [reportAttributeAccessIssue]


# Example usage
if __name__ == "__main__":
    pattern = r"^\d{3}-\d{2}-\d{4}$"
    text = "123-45-6789"

    if match(pattern, text):
        print("Match found!")
    else:
        print("No match.")
