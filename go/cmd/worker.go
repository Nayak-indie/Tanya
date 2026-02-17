package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"
)

type NewsItem struct {
	Title        string   `json:"title"`
	Link         string   `json:"link"`
	Description  string   `json:"description"`
	PubDate      string   `json:"pub_date"`
	Source       string   `json:"source"`
	Category     string   `json:"category"`
	ReadingTime  int      `json:"reading_time"`
	Sentiment    string   `json:"sentiment"`
	Keywords     []string `json:"keywords"`
}

type FeedSource struct {
	Name     string `json:"name"`
	URL      string `json:"url"`
	Category string `json:"category"`
	Enabled  bool   `json:"enabled"`
}

var (
	dataDir    = "../data"
	sourcesURL = []FeedSource{
		{Name: "BBC", URL: "http://feeds.bbci.co.uk/news/world/rss.xml", Category: "World"},
		{Name: "TechCrunch", URL: "https://techcrunch.com/feed/", Category: "Tech"},
		{Name: "HackerNews", URL: "https://hnrss.org/frontpage", Category: "Tech"},
	}
)

// Background worker that fetches news periodically
func worker(interval time.Duration) {
	fmt.Printf("Starting Tanya background worker (Go)...\n")
	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	fetchAll()
	for {
		select {
		case <-ticker.C:
			fetchAll()
		}
	}
}

func fetchAll() {
	fmt.Println("Fetching news from all sources...")
	var allNews []NewsItem

	for _, source := range sourcesURL {
		if !source.Enabled {
			continue
		}
		news := fetchRSS(source)
		allNews = append(allNews, news...)
		fmt.Printf("Fetched %d articles from %s\n", len(news), source.Name)
	}

	saveNews(allNews)
	fmt.Printf("Total: %d articles saved\n", len(allNews))
}

func fetchRSS(source FeedSource) []NewsItem {
	resp, err := http.Get(source.URL)
	if err != nil {
		fmt.Printf("Error fetching %s: %v\n", source.Name, err)
		return nil
	}
	defer resp.Body.Close()

	// Simple XML parsing - in production use proper XML parser
	body, _ := io.ReadAll(resp.Body)
	content := string(body)

	var news []NewsItem
	// Very basic extraction - just a placeholder
	// In reality, parse XML properly
	lines := strings.Split(content, "\n")
	for _, line := range lines {
		if strings.Contains(strings.ToLower(line), "<item>") || strings.Contains(strings.ToLower(line), "<entry>") {
			item := NewsItem{
				Source:      source.Name,
				Category:    source.Category,
				ReadingTime: estimateReadingTime(""),
				Sentiment:   "neutral",
			}
			news = append(news, item)
		}
	}

	return news
}

func estimateReadingTime(content string) int {
	words := len(strings.Fields(content))
	minutes := words / 200
	if minutes < 1 {
		minutes = 1
	}
	return minutes
}

func saveNews(news []NewsItem) {
	data, err := json.MarshalIndent(news, "", "  ")
	if err != nil {
		fmt.Printf("Error marshaling: %v\n", err)
		return
	}
	os.WriteFile(filepath.Join(dataDir, "news.json"), data, 0644)
}

func runRustBinary(name string, args ...string) string {
	cmd := exec.Command(filepath.Join("..", "rust", "target", "release", name), args...)
	output, err := cmd.Output()
	if err != nil {
		return fmt.Sprintf("Error: %v", err)
	}
	return string(output)
}

func main() {
	// Parse flags
	interval := flag.Duration("interval", 15*time.Minute, "Fetch interval")
	once := flag.Bool("once", false, "Fetch once and exit")
	daemon := flag.Bool("daemon", false, "Run as daemon")
	flag.Parse()

	if *daemon || !*once {
		worker(*interval)
		return
	}

	// Default: run once
	fetchAll()
	fmt.Println("\nCalling Rust search engine...")
	fmt.Println(runRustBinary("search", "tech"))
}
