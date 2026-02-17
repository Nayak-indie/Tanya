#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <cctype>

struct NewsItem {
    std::string title;
    std::string link;
    std::string description;
    std::string source;
    std::string category;
    int reading_time;
    std::string sentiment;
    std::vector<std::string> keywords;
};

class DuplicateDetector {
private:
    std::vector<NewsItem> news;
    
    std::string to_lower(const std::string& s) {
        std::string result = s;
        std::transform(result.begin(), result.end(), result.begin(), ::tolower);
        return result;
    }
    
    std::vector<std::string> tokenize(const std::string& s) {
        std::vector<std::string> tokens;
        std::stringstream ss(s);
        std::string word;
        while (ss >> word) {
            tokens.push_back(to_lower(word));
        }
        return tokens;
    }
    
    double jaccard_similarity(const std::vector<std::string>& a, const std::vector<std::string>& b) {
        if (a.empty() && b.empty()) return 1.0;
        if (a.empty() || b.empty()) return 0.0;
        
        std::vector<std::string> set_a = a;
        std::vector<std::string> set_b = b;
        std::sort(set_a.begin(), set_a.end());
        std::sort(set_b.begin(), set_b.end());
        
        std::vector<std::string> intersection;
        std::set_intersection(set_a.begin(), set_a.end(), set_b.begin(), set_b.end(),
                             std::back_inserter(intersection));
        
        std::vector<std::string> union_set = a;
        union_set.insert(union_set.end(), b.begin(), b.end());
        std::sort(union_set.begin(), union_set.end());
        union_set.erase(std::unique(union_set.begin(), union_set.end()), union_set.end());
        
        if (union_set.empty()) return 0.0;
        return (double)intersection.size() / union_set.size();
    }
    
public:
    void load_news(const std::string& filename) {
        std::ifstream file(filename);
        if (!file.is_open()) {
            std::cerr << "Cannot open: " << filename << std::endl;
            return;
        }
        
        std::string line;
        NewsItem item;
        while (std::getline(file, line)) {
            if (line.find("\"title\"") != std::string::npos) {
                size_t start = line.find(":") + 1;
                size_t end = line.find(",", start);
                if (end == std::string::npos) end = line.find("}");
                item.title = line.substr(start, end - start);
                item.title = item.title.substr(1, item.title.length() - 2); // Remove quotes
            }
            if (line.find("\"source\"") != std::string::npos) {
                size_t start = line.find(":") + 1;
                item.source = line.substr(start);
                item.source = item.source.substr(1, item.source.length() - 3);
            }
        }
        news.push_back(item);
    }
    
    std::vector<std::pair<int, int>> find_duplicates(double threshold = 0.7) {
        std::vector<std::pair<int, int>> duplicates;
        
        for (size_t i = 0; i < news.size(); i++) {
            for (size_t j = i + 1; j < news.size(); j++) {
                auto tokens_a = tokenize(news[i].title + " " + news[i].description);
                auto tokens_b = tokenize(news[j].title + " " + news[j].description);
                
                double sim = jaccard_similarity(tokens_a, tokens_b);
                if (sim >= threshold) {
                    duplicates.push_back({(int)i, (int)j});
                }
            }
        }
        return duplicates;
    }
    
    int remove_duplicates(double threshold = 0.7) {
        std::vector<NewsItem> unique;
        int removed = 0;
        
        for (const auto& item : news) {
            bool is_dup = false;
            for (const auto& u : unique) {
                auto tokens_a = tokenize(item.title);
                auto tokens_b = tokenize(u.title);
                if (jaccard_similarity(tokens_a, tokens_b) >= threshold) {
                    is_dup = true;
                    removed++;
                    break;
                }
            }
            if (!is_dup) {
                unique.push_back(item);
            }
        }
        
        news = unique;
        return removed;
    }
    
    void save_news(const std::string& filename) {
        std::ofstream file(filename);
        file << "[\n";
        for (size_t i = 0; i < news.size(); i++) {
            file << "  {\"title\": \"" << news[i].title << "\", ";
            file << "\"source\": \"" << news[i].source << "\"}\n";
            if (i < news.size() - 1) file << ",";
        }
        file << "]\n";
    }
    
    void stats() {
        std::map<std::string, int> by_source;
        std::map<std::string, int> by_category;
        
        for (const auto& item : news) {
            by_source[item.source]++;
            by_category[item.category]++;
        }
        
        std::cout << "=== C++ Statistics ===" << std::endl;
        std::cout << "Total articles: " << news.size() << std::endl;
        std::cout << "\nBy Source:" << std::endl;
        for (const auto& p : by_source) {
            std::cout << "  " << p.first << ": " << p.second << std::endl;
        }
        std::cout << "\nBy Category:" << std::endl;
        for (const auto& p : by_category) {
            std::cout << "  " << p.first << ": " << p.second << std::endl;
        }
    }
};

int main(int argc, char* argv[]) {
    DuplicateDetector detector;
    
    std::string command = (argc > 1) ? argv[1] : "stats";
    
    if (command == "stats") {
        detector.load_news("../data/news.json");
        detector.stats();
    } else if (command == "dedup") {
        double threshold = (argc > 2) ? std::stod(argv[2]) : 0.7;
        detector.load_news("../data/news.json");
        auto dups = detector.find_duplicates(threshold);
        std::cout << "Found " << dups.size() << " duplicate pairs" << std::endl;
    } else if (command == "remove") {
        double threshold = (argc > 2) ? std::stod(argv[2]) : 0.7;
        detector.load_news("../data/news.json");
        int removed = detector.remove_duplicates(threshold);
        detector.save_news("../data/news.json");
        std::cout << "Removed " << removed << " duplicates" << std::endl;
    } else {
        std::cout << "C++ Duplicate Detector" << std::endl;
        std::cout << "Usage: dedup <command> [threshold]" << std::endl;
        std::cout << "Commands: stats, dedup, remove" << std::endl;
    }
    
    return 0;
}