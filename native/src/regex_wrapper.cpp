// regex_wrapper.cpp
#include <regex>
#include <string>
#include <unordered_map>
#include <memory>

// A map to store compiled regex objects
std::unordered_map<int, std::shared_ptr<std::regex>> regex_cache;
int next_id = 0;

extern "C" {
    // Compile a regex pattern and return an ID
    int compile_pattern(const char* pattern) {
        try {
            auto re = std::make_shared<std::regex>(pattern);
            int id = next_id++;
            regex_cache[id] = re;
            return id;
        } catch (const std::regex_error&) {
            return -1; // Return -1 to indicate an error
        }
    }

    // Match a compiled regex against text
    bool match_compiled(int id, const char* text) {
        auto it = regex_cache.find(id);
        if (it != regex_cache.end()) {
            return std::regex_match(text, *it->second);
        }
        return false; // Return false if the ID is not found
    }

    // Release a compiled regex by ID
    void release_compiled(int id) {
        regex_cache.erase(id);
    }

    bool match(const char* pattern, const char* text) {
        try {
            std::regex re(pattern);
            return std::regex_match(text, re);
        } catch (const std::regex_error&) {
            return false;
        }
    }
}
