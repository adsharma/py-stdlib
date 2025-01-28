// regex_wrapper.cpp
#include <regex>
#include <string>
#include <unordered_map>
#include <vector>
#include <memory>
#include <cstring>

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

    // Search for a regex pattern in a string
    const char* search_pattern(int id, const char* text) {
        auto it = regex_cache.find(id);
        if (it == regex_cache.end()) {
            return nullptr; // Return nullptr if the ID is not found
        }

        std::smatch match;
        std::string str(text);
        if (std::regex_search(str, match, *it->second)) {
            return strdup(match.str().c_str()); // Return the matched substring
        }
        return nullptr; // Return nullptr if no match is found
    }


    // Find all matches of a regex pattern in a string
    extern "C" char** findall_pattern(int id, const char* text) {
        auto it = regex_cache.find(id);
        if (it == regex_cache.end()) {
            return nullptr; // Return nullptr if the ID is not found
        }

        std::string str(text);
        std::smatch match;
        std::vector<std::string> matches;
        std::string::const_iterator searchStart(str.cbegin());

        // Find all matches
        while (std::regex_search(searchStart, str.cend(), match, *it->second)) {
            matches.push_back(match.str()); // Store each match in the vector
            searchStart = match.suffix().first;
        }

        if (matches.empty()) {
            return nullptr; // Return nullptr if no matches are found
        }

        // Allocate an array of char* to hold the matches
        char** result = (char**)malloc((matches.size() + 1) * sizeof(char*));
        if (!result) {
            return nullptr; // Return nullptr if memory allocation fails
        }

        // Copy each match into the array
        for (size_t i = 0; i < matches.size(); ++i) {
            result[i] = strdup(matches[i].c_str()); // Duplicate the string
            if (!result[i]) {
                // Free previously allocated memory if strdup fails
                for (size_t j = 0; j < i; ++j) {
                    free(result[j]);
                }
                free(result);
                return nullptr;
            }
        }

        // Null-terminate the array
        result[matches.size()] = nullptr;

        return result;
    }

    // Function to free the allocated memory for the matches
    extern "C" void free_matches(char** matches) {
        if (!matches) {
            return;
        }

        for (size_t i = 0; matches[i] != nullptr; ++i) {
            free(matches[i]); // Free each string
        }
        free(matches); // Free the array itself
    }

    // Substitute all occurrences of a regex pattern in a string
    const char* substitute_pattern(int id, const char* text, const char* replacement) {
        auto it = regex_cache.find(id);
        if (it == regex_cache.end()) {
            return nullptr; // Return nullptr if the ID is not found
        }

        std::string str(text);
        std::string result = std::regex_replace(str, *it->second, replacement);
        return strdup(result.c_str()); // Return the modified string
    }
}
