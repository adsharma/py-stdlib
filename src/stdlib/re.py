from stdlib._cffi_util import load_library

# Define the C interface
interface = """
    int compile_pattern(const char* pattern);
    bool match_compiled(int id, const char* text);
    void release_compiled(int id);
    bool match(const char* pattern, const char* text);
"""

# Load the shared library
lib = load_library("regex_wrapper", interface)


def match(pattern: str, text: str) -> bool:
    return lib.match(  # pyright: ignore [reportAttributeAccessIssue]
        pattern.encode("utf-8"), text.encode("utf-8")
    )


# Python wrapper class
class CompiledRegex:
    def __init__(self, pattern):
        self.id = lib.compile_pattern(
            pattern.encode("utf-8")
        )  # pyright: ignore [reportAttributeAccessIssue]
        if self.id == -1:
            raise ValueError("Invalid regex pattern")

    def match(self, text):
        return lib.match_compiled(
            self.id, text.encode("utf-8")
        )  # pyright: ignore [reportAttributeAccessIssue]

    def __del__(self):
        lib.release_compiled(self.id)  # pyright: ignore [reportAttributeAccessIssue]


def compile(pattern: str) -> CompiledRegex:
    return CompiledRegex(pattern)


# Example usage
if __name__ == "__main__":
    pattern = r"^\d{3}-\d{2}-\d{4}$"
    text = "123-45-6789"

    if match(pattern, text):
        print("Match found!")
    else:
        print("No match.")
