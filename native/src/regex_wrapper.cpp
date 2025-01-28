// regex_wrapper.cpp
#include <regex>
#include <string>

extern "C" {
    bool match(const char* pattern, const char* text) {
        try {
            std::regex re(pattern);
            return std::regex_match(text, re);
        } catch (const std::regex_error&) {
            return false;
        }
    }
}
