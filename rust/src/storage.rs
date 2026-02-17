//! Storage - JSON file operations in Rust
//! Build: cd rust && cargo build --release
//! Run:   ./target/release storage <command> [args]

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::env;
use std::fs::{self, File};
use std::io::{Read, Write};
use std::path::Path;

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

#[derive(Debug, Serialize, Deserialize, Default)]
pub struct Storage {
    pub news: Vec<NewsItem>,
    pub favorites: Vec<String>,
    pub sources: Vec<FeedSource>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct FeedSource {
    pub name: String,
    pub url: String,
    pub category: String,
    pub enabled: bool,
}

fn get_storage_path() -> PathBuf {
    Path::new("../data/news.json").to_path_buf()
}

fn load_storage() -> Storage {
    let path = get_storage_path();
    if let Ok(mut file) = File::open(&path) {
        let mut content = String::new();
        if file.read_to_string(&mut content).is_ok() {
            if let Ok(storage) = serde_json::from_str(&content) {
                return storage;
            }
        }
    }
    Storage::default()
}

fn save_storage(storage: &Storage) -> Result<(), String> {
    let path = get_storage_path();
    let json = serde_json::to_string_pretty(storage).map_err(|e| e.to_string())?;
    let mut file = File::create(&path).map_err(|e| e.to_string())?;
    file.write_all(json.as_bytes()).map_err(|e| e.to_string())?;
    Ok(())
}

fn add_item(item: NewsItem) {
    let mut storage = load_storage();
    storage.news.retain(|i| i.link != item.link);
    storage.news.insert(0, item);
    if storage.news.len() > 1000 {
        storage.news.truncate(1000);
    }
    save_storage(&storage).expect("Failed to save");
}

fn list_news(limit: usize) {
    let storage = load_storage();
    for (i, item) in storage.news.iter().enumerate().take(limit) {
        println!("[{}] {} - {}", i + 1, item.source, item.title);
        println!("    Category: {} | Sentiment: {} | Read time: {} min", 
                 item.category, item.sentiment, item.reading_time);
    }
}

fn search(query: &str) {
    let storage = load_storage();
    let query_lower = query.to_lowercase();
    for item in &storage.news {
        if item.title.to_lowercase().contains(&query_lower) || 
           item.description.to_lowercase().contains(&query_lower) {
            println!("{} | {}", item.source, item.title);
        }
    }
}

fn add_favorite(link: &str) {
    let mut storage = load_storage();
    if !storage.favorites.contains(&link.to_string()) {
        storage.favorites.push(link.to_string());
        save_storage(&storage).expect("Failed to save");
        println!("Added to favorites");
    }
}

fn list_favorites() {
    let storage = load_storage();
    println!("=== Favorites ({}) ===", storage.favorites.len());
    for link in &storage.favorites {
        println!("{}", link);
    }
}

fn clear_news() {
    let mut storage = load_storage();
    storage.news.clear();
    save_storage(&storage).expect("Failed to save");
    println!("Cleared all news");
}

fn stats() {
    let storage = load_storage();
    let mut by_category: HashMap<String, usize> = HashMap::new();
    let mut by_source: HashMap<String, usize> = HashMap::new();
    let mut by_sentiment: HashMap<String, usize> = HashMap::new();
    
    for item in &storage.news {
        *by_category.entry(item.category.clone()).or_insert(0) += 1;
        *by_source.entry(item.source.clone()).or_insert(0) += 1;
        *by_sentiment.entry(item.sentiment.clone()).or_insert(0) += 1;
    }
    
    println!("=== Tanya Statistics ===");
    println!("Total articles: {}", storage.news.len());
    println!("Favorites: {}", storage.favorites.len());
    println!("\nBy Category:");
    for (cat, count) in by_category {
        println!("  {}: {}", cat, count);
    }
    println!("\nBy Sentiment:");
    for (sent, count) in by_sentiment {
        println!("  {}: {}", sent, count);
    }
}

use std::path::PathBuf;

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 {
        println!("Tanya Storage (Rust)");
        println!("Usage: storage <command>");
        println!("Commands:");
        println!("  add <json>       Add news item from JSON");
        println!("  list [N]         List N news items (default 10)");
        println!("  search <query>   Search news");
        println!("  fav <link>       Add to favorites");
        println!("  favorites        List favorites");
        println!("  stats            Show statistics");
        println!("  clear            Clear all news");
        return;
    }
    
    match args[1].as_str() {
        "list" => {
            let limit = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(10);
            list_news(limit);
        }
        "add" => {
            if let Some(json) = args.get(2) {
                if let Ok(item) = serde_json::from_str::<NewsItem>(json) {
                    add_item(item);
                    println!("Added item");
                } else {
                    eprintln!("Invalid JSON");
                }
            }
        }
        "search" => {
            if let Some(query) = args.get(2) {
                search(query);
            }
        }
        "fav" => {
            if let Some(link) = args.get(2) {
                add_favorite(link);
            }
        }
        "favorites" => list_favorites(),
        "stats" => stats(),
        "clear" => clear_news(),
        _ => println!("Unknown command: {}", args[1]),
    }
}