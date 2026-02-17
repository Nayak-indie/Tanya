/**
 * Tanya - Core News Processor (C++)
 * High-performance article processing engine
 */

#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <cmath>
#include <ctime>
#include <sstream>
#include <iomanip>

namespace taya {

struct Article {
    std::string id;
    std::string title;
    std::string link;
    std::string published;
    std::string content;
    std::vector<std::string> keywords;
    std::string sentiment;
    bool is_favorite = false;
    time_t saved_at = 0;
};

class NewsProcessor {
private:
    std::vector<Article> articles;
    std::unordered_map<std::string, std::vector<std::string>> keyword_index;

public:
    void add_article(const Article& article) {
        articles.push_back(article);
    }

    float similarity(const Article& a, const Article& b) {
        std::vector<std::string> common;
        for (const auto& kw : a.keywords) {
            if (std::find(b.keywords.begin(), b.keywords.end(), kw) != b.keywords.end()) {
                common.push_back(kw);
            }
        }
        float union_size = a.keywords.size() + b.keywords.size() - common.size();
        if (union_size == 0) return 0.0f;
        return static_cast<float>(common.size()) / union_size;
    }

    std::vector<std::pair<std::string, std::string>> find_duplicates(float threshold = 0.8f) {
        std::vector<std::pair<std::string, std::string>> duplicates;
        for (size_t i = 0; i < articles.size(); ++i) {
            for (size_t j = i + 1; j < articles.size(); ++j) {
                if (similarity(articles[i], articles[j]) >= threshold) {
                    duplicates.push_back({articles[i].id, articles[j].id});
                }
            }
        }
        return duplicates;
    }

    std::vector<Article> get_favorites() {
        std::vector<Article> result;
        for (const auto& a : articles) if (a.is_favorite) result.push_back(a);
        return result;
    }

    void toggle_favorite(const std::string& id) {
        for (auto& a : articles) if (a.id == id) a.is_favorite = !a.is_favorite;
    }

    size_t size() const { return articles.size(); }
};

int reading_time(const std::string& content, int wpm = 200) {
    int words = 0;
    for (size_t i = 0; i < content.size(); ++i) {
        if (isalpha(content[i])) {
            while (i < content.size() && isalpha(content[i])) ++i;
            ++words;
        }
    }
    return std::max(1, (int)std::ceil((float)words / wpm));
}

std::string analyze_sentiment(const std::string& text) {
    std::unordered_map<std::string, int> pos = {{"good", 1}, {"great", 2}, {"excellent", 3}, {"success", 2}};
    std::unordered_map<std::string, int> neg = {{"bad", -1}, {"terrible", -3}, {"failure", -2}, {"crisis", -2}};
    
    std::string word;
    int score = 0;
    for (char c : text) {
        if (isalpha(c)) word += tolower(c);
        else {
            if (pos.count(word)) score += pos[word];
            if (neg.count(word)) score += neg[word];
            word.clear();
        }
    }
    if (score > 0) return "positive";
    if (score < 0) return "negative";
    return "neutral";
}

} // namespace taya

extern "C" {
    void* create_processor() { return new taya::NewsProcessor(); }
    void destroy_processor(void* p) { delete static_cast<taya::NewsProcessor*>(p); }
    int get_reading_time(const char* content) { return taya::reading_time(content); }
    const char* get_sentiment(const char* text) { static std::string r; r = taya::analyze_sentiment(text); return r.c_str(); }
}

int main() {
    taya::Article a{"1", "AI Breakthrough", "https://x.com", "", "Great success in AI research", {"AI", "research"}, "neutral"};
    std::cout << "Reading time: " << taya::reading_time(a.content) << " min\n";
    std::cout << "Sentiment: " << taya::analyze_sentiment(a.content) << "\n";
    return 0;
}
