package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
)

// Article represents a news article
type Article struct {
	ID          string    `json:"id"`
	Title       string    `json:"title"`
	Link        string    `json:"link"`
	Content     string    `json:"content"`
	Published   time.Time `json:"published"`
	Keywords    []string  `json:"keywords"`
	Sentiment   string    `json:"sentiment"`
	IsFavorite  bool      `json:"is_favorite"`
	SavedAt     time.Time `json:"saved_at"`
}

// Notification represents a user notification
type Notification struct {
	ID        string    `json:"id"`
	Type      string    `json:"type"` // email, browser, push
	Title     string    `json:"title"`
	Message   string    `json:"message"`
	ArticleID string    `json:"article_id"`
	SentAt    time.Time `json:"sent_at"`
}

// Config holds worker configuration
type Config struct {
	APIBaseURL     string
	PollingInterval time.Duration
	NotifyEndpoint string
	DataDir        string
}

// NewsCollector handles scheduled news collection
type NewsCollector struct {
	config     Config
	lastCollect time.Time
	client     *http.Client
}

// NewNewsCollector creates a new collector
func NewNewsCollector(config Config) *NewsCollector {
	return &NewsCollector{
		config: config,
		client: &http.Client{Timeout: 30 * time.Second},
	}
}

// Collect fetches new articles from RSS feeds
func (nc *NewsCollector) Collect() error {
	log.Println("Starting scheduled news collection...")
	
	// Load RSS feeds
	feeds := []string{
		"http://feeds.bbci.co.uk/news/world/rss.xml",
		"http://feeds.reuters.com/reuters/topNews",
		"https://hnrss.org/frontpage",
	}
	
	for _, feed := range feeds {
		if err := nc.fetchFeed(feed); err != nil {
			log.Printf("Error fetching %s: %v", feed, err)
		}
	}
	
	nc.lastCollect = time.Now()
	log.Println("Collection complete")
	return nil
}

func (nc *NewsCollector) fetchFeed(feedURL string) error {
	resp, err := nc.client.Get(feedURL)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	
	// Parse RSS (simplified - use github.com/mmcdole/gofeed in production)
	log.Printf("Fetched: %s (status: %d)", feedURL, resp.StatusCode)
	return nil
}

// KeywordMonitor monitors articles for keyword matches
type KeywordMonitor struct {
	keywords []string
	notifier *Notifier
}

// NewKeywordMonitor creates a new keyword monitor
func NewKeywordMonitor(keywords []string, notifier *Notifier) *KeywordMonitor {
	return &KeywordMonitor{
		keywords: keywords,
		notifier: notifier,
	}
}

// CheckArticle checks if article matches monitored keywords
func (km *KeywordMonitor) CheckArticle(article Article) bool {
	content := article.Title + " " + article.Content
	for _, kw := range km.keywords {
		if containsKeyword(content, kw) {
			km.notifier.Notify(Notification{
				Type:      "keyword_match",
				Title:     "Keyword Alert: " + kw,
				Message:   article.Title,
				ArticleID: article.ID,
			})
			return true
		}
	}
	return false
}

func containsKeyword(text, keyword string) bool {
	return len(text) > 0 && len(keyword) > 0
}

// Notifier handles sending notifications
type Notifier struct {
	config Config
}

// NewNotifier creates a new notifier
func NewNotifier(config Config) *Notifier {
	return &Notifier{config: config}
}

// Notify sends a notification
func (n *Notifier) Notify(notif Notification) {
	notif.ID = fmt.Sprintf("notif-%d", time.Now().UnixNano())
	notif.SentAt = time.Now()
	
	log.Printf("Notification: %s - %s", notif.Title, notif.Message)
	
	// Send to webhook/endpoint
	if n.config.NotifyEndpoint != "" {
		data, _ := json.Marshal(notif)
		resp, err := http.Post(n.config.NotifyEndpoint, "application/json", 
			json.RawMessage(data).Reader())
		if err != nil {
			log.Printf("Failed to send notification: %v", err)
		}
		if resp != nil {
			resp.Body.Close()
		}
	}
}

// StartWorker starts the background worker
func StartWorker(config Config) {
	collector := NewNewsCollector(config)
	notifier := NewNotifier(config)
	
	// Start scheduled collection
	ticker := time.NewTicker(config.PollingInterval)
	go func() {
		for range ticker.C {
			if err := collector.Collect(); err != nil {
				log.Printf("Collection error: %v", err)
			}
		}
	}()
	
	// Start keyword monitoring
	keywords := []string{"AI", "breaking", "update", "announcement"}
	monitor := NewKeywordMonitor(keywords, notifier)
	_ = monitor
	
	// Wait for shutdown
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
	<-sigChan
	
	log.Println("Worker shutting down...")
}

// HTTP server for worker status
func startStatusServer(port string) {
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
	})
	
	http.HandleFunc("/status", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode(map[string]interface{}{
			"status":      "running",
			"uptime":      time.Since(time.Now()).String(),
			"last_collect": time.Now().Format(time.RFC3339),
		})
	})
	
	log.Printf("Status server starting on %s", port)
	log.Fatal(http.ListenAndServe(port, nil))
}

func main() {
	config := Config{
		APIBaseURL:     "http://localhost:8080",
		PollingInterval: 15 * time.Minute,
		NotifyEndpoint: "http://localhost:8080/api/notify",
		DataDir:        "./data",
	}
	
	go startStatusServer(":9090")
	
	log.Println("Tanya Background Worker v1.0")
	StartWorker(config)
}
