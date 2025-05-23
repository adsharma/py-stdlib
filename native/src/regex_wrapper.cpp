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
    // Behavior depends on the number of capture groups in the regex:
    // 0 groups: returns list of full matches.
    // 1 group: returns list of strings for that group.
    // >1 groups: returns list of strings, where each string is a concatenation of all captured groups for a match, delimited by SOH (\x01).
    extern "C" char** findall_pattern(int id, const char* text) {
        auto it = regex_cache.find(id);
        if (it == regex_cache.end()) {
            return nullptr;
        }

        std::shared_ptr<std::regex> re = it->second;
        size_t num_groups = re->mark_count(); // Number of capture groups

        std::string s_text(text);
        std::vector<std::string> collected_matches;
        auto search_start = s_text.cbegin();
        std::smatch current_match;

        while (std::regex_search(search_start, s_text.cend(), current_match, *re)) {
            if (num_groups == 0) { // No groups, return full match
                collected_matches.push_back(current_match[0].str());
            } else if (num_groups == 1) { // One group, return group 1
                collected_matches.push_back(current_match[1].str());
            } else { // More than one group
                std::string combined_groups_str;
                for (size_t i = 1; i <= num_groups; ++i) { // Iterate from group 1 to num_groups
                    combined_groups_str += current_match[i].str();
                    if (i < num_groups) {
                        combined_groups_str += '\x01'; // Delimiter
                    }
                }
                collected_matches.push_back(combined_groups_str);
            }
            search_start = current_match.suffix().first;
            if (search_start == s_text.cbegin() && current_match[0].length() == 0) {
                 // Handle empty match at the beginning of the remaining string to avoid infinite loop.
                 // This can happen with patterns like "a*". Advance by one character.
                 if (search_start != s_text.cend()) {
                    search_start++;
                 } else {
                    break; // Reached end of string
                 }
            }

        }

        if (collected_matches.empty()) {
            return nullptr;
        }

        char** result_array = (char**)malloc((collected_matches.size() + 1) * sizeof(char*));
        if (!result_array) {
            return nullptr;
        }

        for (size_t i = 0; i < collected_matches.size(); ++i) {
            result_array[i] = strdup(collected_matches[i].c_str());
            if (!result_array[i]) {
                for (size_t j = 0; j < i; ++j) free(result_array[j]);
                free(result_array);
                return nullptr;
            }
        }
        result_array[collected_matches.size()] = nullptr; // Null-terminate

        return result_array;
    }

    // Function to free the allocated memory for the matches (used by findall_pattern)
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
