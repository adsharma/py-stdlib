import cffi

from stdlib._cffi_util import load_library

# Define the C interface
interface = """
    int compile_pattern(const char* pattern);
    bool match_compiled(int id, const char* text);
    void release_compiled(int id);
    bool match(const char* pattern, const char* text);
    const char* search_pattern(int id, const char* text);
    char** findall_pattern(int id, const char* text);
    void free_matches(char** matches);
    const char* substitute_pattern(int id, const char* text, const char* replacement);
    void free(void *ptr);
"""

# Load the shared library
ffi = cffi.FFI()
lib = load_library("regex_wrapper", interface)


def match(pattern: str, text: str) -> bool:
    return lib.match(  # pyright: ignore [reportAttributeAccessIssue]
        pattern.encode("utf-8"), text.encode("utf-8")
    )


# Python wrapper class
class CompiledRegex:
    def __init__(self, pattern):
        self.id = lib.compile_pattern(pattern.encode("utf-8"))  # type: ignore
        if self.id == -1:
            raise ValueError("Invalid regex pattern")

    def match(self, text):
        return lib.match_compiled(self.id, text.encode("utf-8"))  # type: ignore

    def __del__(self):
        lib.release_compiled(self.id)  # type: ignore

    def search(self, text: str) -> str | None:
        # Search for the compiled regex in the text
        result = lib.search_pattern(self.id, text.encode("utf-8"))  # type: ignore
        if result:
            ptr = result
            try:
                result_bytes: bytes = ffi.string(result)
                return result_bytes.decode("utf-8")
            finally:
                lib.free(ptr)
        return None

    def findall(self, text: str) -> list[str]:
        # Find all matches of the compiled regex in the text
        matches_ptr = lib.findall_pattern(self.id, text.encode("utf-8"))  # type: ignore
        matches = []
        if matches_ptr:
            try:
                # Convert the array of C strings to a Python list
                i = 0
                while matches_ptr[i]:
                    matches.append(ffi.string(matches_ptr[i]).decode("utf-8"))
                    i += 1
            finally:
                # Free the allocated memory
                lib.free_matches(matches_ptr)
        return matches

    def sub(self, replacement: str, text: str) -> str:
        # Substitute all occurrences of the compiled regex in the text
        result = lib.substitute_pattern(  # type: ignore
            self.id, text.encode("utf-8"), replacement.encode("utf-8")
        )
        if result:
            ptr = result
            try:
                result_bytes: bytes = ffi.string(result)
                return result_bytes.decode("utf-8")
            finally:
                lib.free(ptr)
        return text  # Return the original text if substitution fails


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
