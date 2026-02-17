/* Tanya RSS Parser in C
 * Build: gcc -o bin/rss_parser c/rss_parser.c -lcurl -lxml2
 * Run: ./bin/rss_parser <url>
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include <libxml/parser.h>
#include <libxml/tree.h>

#define MAX_TITLE 500
#define MAX_DESC 2000
#define MAX_URL 1000

typedef struct {
    char title[MAX_TITLE];
    char link[MAX_URL];
    char description[MAX_DESC];
    char pubdate[100];
    char category[50];
} RSSItem;

typedef struct {
    RSSItem *items;
    size_t count;
    size_t capacity;
} RSSFeed;

void init_feed(RSSFeed *feed) {
    feed->capacity = 100;
    feed->count = 0;
    feed->items = malloc(sizeof(RSSItem) * feed->capacity);
}

void add_item(RSSFeed *feed, RSSItem *item) {
    if (feed->count >= feed->capacity) {
        feed->capacity *= 2;
        feed->items = realloc(feed->items, sizeof(RSSItem) * feed->capacity);
    }
    feed->items[feed->count++] = *item;
}

size_t write_callback(void *contents, size_t size, size_t nmemb, void *userp) {
    size_t realsize = size * nmemb;
    char **buffer = (char **)userp;
    *buffer = realloc(*buffer, realsize + 1);
    memcpy(*buffer, contents, realsize);
    (*buffer)[realsize] = 0;
    return realsize;
}

char* fetch_url(const char *url) {
    CURL *curl;
    CURLcode res;
    char *buffer = malloc(1);
    buffer[0] = '\0';
    
    curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &buffer);
        curl_easy_setopt(curl, CURLOPT_USERAGENT, "Tanya/1.0 RSS Parser (C)");
        
        res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            fprintf(stderr, "curl error: %s\n", curl_easy_strerror(res));
            free(buffer);
            return NULL;
        }
        curl_easy_cleanup(curl);
    }
    return buffer;
}

void extract_tag(const char *xml, const char *tag, char *output, size_t max) {
    char open_tag[100], close_tag[100];
    snprintf(open_tag, sizeof(open_tag), "<%s>", tag);
    snprintf(close_tag, sizeof(close_tag), "</%s>", tag);
    
    char *start = strstr(xml, open_tag);
    if (!start) {
        output[0] = '\0';
        return;
    }
    start += strlen(open_tag);
    
    char *end = strstr(start, close_tag);
    if (!end) {
        output[0] = '\0';
        return;
    }
    
    size_t len = end - start;
    if (len >= max) len = max - 1;
    
    strncpy(output, start, len);
    output[len] = '\0';
}

int is_rss(const char *xml) {
    return strstr(xml, "<rss") != NULL || strstr(xml, "<channel>") != NULL;
}

int is_atom(const char *xml) {
    return strstr(xml, "<feed") != NULL;
}

void parse_rss(const char *xml, RSSFeed *feed) {
    const char *ptr = xml;
    
    while ((ptr = strstr(ptr, "<item>")) != NULL) {
        RSSItem item = {0};
        
        extract_tag(ptr, "title", item.title, MAX_TITLE);
        extract_tag(ptr, "link", item.link, MAX_URL);
        extract_tag(ptr, "description", item.description, MAX_DESC);
        extract_tag(ptr, "pubDate", item.pubdate, 100);
        extract_tag(ptr, "category", item.category, 50);
        
        if (item.title[0] != '\0') {
            add_item(feed, &item);
        }
        ptr++;
    }
}

void categorize(RSSItem *item) {
    const char *text = item->title;
    if (strstr(text, "AI") || strstr(text, "artificial intelligence")) {
        strcpy(item->category, "AI");
    } else if (strstr(text, "tech") || strstr(text, "software")) {
        strcpy(item->category, "Tech");
    } else if (strstr(text, "stock") || strstr(text, "market")) {
        strcpy(item->category, "Finance");
    } else if (strstr(text, "war") || strstr(text, "military")) {
        strcpy(item->category, "World");
    } else if (strstr(text, "science") || strstr(text, "space")) {
        strcpy(item->category, "Science");
    }
}

int estimate_reading_time(const char *text) {
    int words = 0;
    int in_word = 0;
    for (int i = 0; text[i]; i++) {
        if (text[i] == ' ' || text[i] == '\n') {
            in_word = 0;
        } else if (!in_word) {
            in_word = 1;
            words++;
        }
    }
    return words / 200 + 1;
}

const char* analyze_sentiment(const char *title, const char *desc) {
    const char *text = strstr(title, desc) ? title : "";  // simplified
    int pos = 0, neg = 0;
    
    const char *positive[] = {"good", "great", "excellent", "amazing", "breakthrough"};
    const char *negative[] = {"bad", "terrible", "crisis", "fail", "death", "war"};
    
    for (int i = 0; i < 5; i++) {
        if (strstr(text, positive[i])) pos++;
    }
    for (int i = 0; i < 6; i++) {
        if (strstr(text, negative[i])) neg++;
    }
    
    if (pos > neg) return "positive";
    if (neg > pos) return "negative";
    return "neutral";
}

void print_feed(RSSFeed *feed) {
    printf("Tanya RSS Parser (C)\n");
    printf("====================\n\n");
    printf("Found %zu articles:\n\n", feed->count);
    
    for (size_t i = 0; i < feed->count && i < 10; i++) {
        RSSItem *item = &feed->items[i];
        categorize(item);
        
        printf("[%zu] %s\n", i+1, item->title);
        printf("    Source: %s | Category: %s | Read time: %d min\n",
               item->category[0] ? item->category : "General",
               item->category,
               estimate_reading_time(item->description));
        if (item->link[0])
            printf("    Link: %s\n", item->link);
        printf("\n");
    }
}

int main(int argc, char *argv[]) {
    const char *url = "http://feeds.bbci.co.uk/news/world/rss.xml";
    
    if (argc > 1) {
        if (strcmp(argv[1], "--help") == 0) {
            printf("Tanya RSS Parser (C)\n");
            printf("Usage: rss_parser [url]\n");
            return 0;
        }
        url = argv[1];
    }
    
    printf("Fetching %s...\n", url);
    
    char *xml = fetch_url(url);
    if (!xml) {
        fprintf(stderr, "Failed to fetch URL\n");
        return 1;
    }
    
    if (!is_rss(xml) && !is_atom(xml)) {
        fprintf(stderr, "Not a valid RSS/Atom feed\n");
        free(xml);
        return 1;
    }
    
    RSSFeed feed;
    init_feed(&feed);
    parse_rss(xml, &feed);
    print_feed(&feed);
    
    free(feed.items);
    free(xml);
    
    printf("Engine: C (high performance)\n");
    
    return 0;
}
