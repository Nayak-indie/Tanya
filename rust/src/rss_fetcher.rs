//! RSS Fetcher - Fetches and parses RSS/Atom feeds
//! Build: cd rust && cargo build --release
//! Run:   ./target/release/rss_fetcher <feed_url>

use rss::{Channel, ChannelBuilder, Item, ItemBuilder};
use serde::{Deserialize, Serialize};
use std::env;
use std::fs;
use std::io::Write;

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct NewsItem {
    pub title: String,
    pub link: String,
    pub description: String,
    pub pub_date: String,
    pub source: String,
    pub category: String,
    pub reading_time: u32,
    pub sentiment: String,
    pub keywords: Vec<String>,
}

fn estimate_reading_time(content: &str) -> u32 {
    let words: Vec<&str> = content.split_whitespace().collect();
    let minutes = (words.len() as f64 / 200.0).ceil() as u32;
    minutes.max(1)
}

fn extract_keywords(title: &str, desc: &str) -> Vec<String> {
    let text = format!("{} {}", title, desc);
    let stop_words = ["the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", 
                      "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
                      "being", "have", "has", "had", "do", "does", "did", "will", "would",
                      "could", "should", "may", "might", "must", "shall", "can", "need",
                      "dare", "ought", "used", "this", "that", "these", "those", "it", "its"];
    
    let words: Vec<String> = text.to_lowercase()
        .split(|c: char| !c.is_alphanumeric())
        .filter(|w| w.len() > 3)
        .filter(|w| !stop_words.contains(w))
        .map(|w| w.to_string())
        .collect();
    
    let mut word_count: std::collections::HashMap<String, u32> = std::collections::HashMap::new();
    for word in words {
        *word_count.entry(word).or_insert(0) += 1;
    }
    
    let mut keywords: Vec<String> = word_count.into_iter()
        .filter(|(_, count)| *count > 1)
        .map(|(word, _)| word)
        .take(10)
        .collect();
    
    keywords.sort();
    keywords
}

fn analyze_sentiment(title: &str, desc: &str) -> String {
    let text = format!("{} {}", title, desc).to_lowercase();
    
    let positive = ["good", "great", "excellent", "amazing", "breakthrough", "success", 
                    "win", "achievement", "improve", "positive", "growth", "hero", "best"];
    let negative = ["bad", "terrible", "crisis", "fail", "death", "war", "attack", "disaster",
                    "loss", "fear", "worse", "worst", "kill", "destroy", "threat"];
    
    let pos_count = positive.iter().filter(|w| text.contains(*w)).count();
    let neg_count = negative.iter().filter(|w| text.contains(*w)).count();
    
    if pos_count > neg_count {
        "positive".to_string()
    } else if neg_count > pos_count {
        "negative".to_string()
    } else {
        "neutral".to_string()
    }
}

fn infer_category(title: &str, desc: &str) -> String {
    let text = format!("{} {}", title, desc).to_lowercase();
    
    if text.contains("ai") || text.contains("artificial intelligence") || text.contains("machine learning") || text.contains("chatgpt") {
        "AI".to_string()
    } else if text.contains("tech") || text.contains("software") || text.contains("google") || text.contains("microsoft") || text.contains("apple") {
        "Tech".to_string()
    } else if text.contains("stock") || text.contains("market") || text.contains("economy") || text.contains("bitcoin") || text.contains("crypto") {
        "Finance".to_string()
    } else if text.contains("climate") || text.contains("weather") || text.contains("environment") || text.contains("storm") {
        "Weather".to_string()
    } else if text.contains("war") || text.contains("military") || text.contains("russia") || text.contains("ukraine") || text.contains("iran") {
        "World".to_string()
    } else if text.contains("science") || text.contains("space") || text.contains("nasa") || text.contains("research") {
        "Science".to_string()
    } else {
        "General".to_string()
    }
}

fn fetch_feed(url: &str) -> Result<Channel, String> {
    let client = reqwest::blocking::Client::builder()
        .timeout(std::time::Duration::from_secs(30))
        .build()
        .map_err(|e| e.to_string())?;
    
    let response = client.get(url)
        .header("User-Agent", "Tanya/1.0 RSS Reader")
        .send()
        .map_err(|e| e.to_string())?;
    
    let content = response.bytes().map_err(|e| e.to_string())?;
    Channel::read_from(&content[..]).map_err(|e| e.to_string())
}

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 {
        // List sources from JSON
        let sources = load_sources();
        for source in sources {
            match fetch_feed(&source.url) {
                Ok(channel) => {
                    for item in channel.items() {
                        let news_item = process_item(item, &source.name);
                        println!("{}", serde_json::to_string(&news_item).unwrap_or_default());
                    }
                }
                Err(e) => {
                    eprintln!("Error fetching {}: {}", source.name, e);
                }
            }
        }
    } else if args[1] == "--help" {
        println!("Tanya RSS Fetcher");
        println!("Usage:");
        println!("  rss_fetcher              # Fetch all configured sources");
        println!("  rss_fetcher <url>        # Fetch single feed");
        println!("  rss_fetcher --list       # List configured sources");
    } else if args[1] == "--list" {
        let sources = load_sources();
        for source in sources {
            println!("{}: {}", source.name, source.url);
        }
    } else {
        // Fetch single URL
        match fetch_feed(&args[1]) {
            Ok(channel) => {
                for item in channel.items() {
                    let news_item = process_item(item, &channel.title().unwrap_or("Unknown").to_string());
                    println!("{}", serde_json::to_string(&news_item).unwrap_or_default());
                }
            }
            Err(e) => {
                eprintln!("Error: {}", e);
                std::process::exit(1);
            }
        }
    }
}

fn load_sources() -> Vec<FeedSource> {
    let sources_file = std::path::Path::new("../data/sources.json");
    if let Ok(content) = fs::read_to_string(sources_file) {
        if let Ok(sources) = serde_json::from_str::<Vec<FeedSource>>(&content) {
            return sources;
        }
    }
    
    // Default sources
    vec![
        FeedSource { name: "BBC".to_string(), url: "http://feeds.bbci.co.uk/news/world/rss.xml".to_string(), category: "World".to_string() },
        FeedSource { name: "Reuters".to_string(), url: "https://www.reutersagency.com/feed/".to_string(), category: "World".to_string() },
        FeedSource { name: "TechCrunch".to_string(), url: "https://techcrunch.com/feed/".to_string(), category: "Tech".to_string() },
    ]
}

#[derive(Debug, Serialize, Deserialize)]
struct FeedSource {
    name: String,
    url: String,
    category: String,
}

fn process_item(item: &Item, source: &str) -> NewsItem {
    let title = item.title().unwrap_or("No title").to_string();
    let desc = item.description().unwrap_or("").to_string();
    let link = item.link().unwrap_or("").to_string();
    let pub_date = item.pub_date().unwrap_or("").to_string();
    
    let reading_time = estimate_reading_time(&desc);
    let sentiment = analyze_sentiment(&title, &desc);
    let keywords = extract_keywords(&title, &desc);
    let category = infer_category(&title, &desc);
    
    NewsItem {
        title,
        link,
        description: desc,
        pub_date,
        source: source.to_string(),
        category,
        reading_time,
        sentiment,
        keywords,
    }
}