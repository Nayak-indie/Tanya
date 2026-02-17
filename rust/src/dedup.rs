//! Duplicate Detection - Find similar articles using Rust
//! Build: cd rust && cargo build --release
//! Run:   ./target/release/dedup [--threshold N]

use similar::{ChangeTag, TextDiff};
use serde::{Deserialize, Serialize};
use std::collections::HashSet;
use std::env;
use std::fs::File;
use std::io::Read;

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct NewsItem {
    pub title: String,
    pub link: String,
    pub description: String,
    pub source: String,
    pub category: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct Storage {
    news: Vec<NewsItem>,
}

fn load_news() -> Vec<NewsItem> {
    let path = std::path::Path::new("../data/news.json");
    if let Ok(mut file) = File::open(path) {
        let mut content = String::new();
        if file.read_to_string(&mut content).is_ok() {
            if let Ok(storage) = serde_json::from_str::<Storage>(&content) {
                return storage.news;
            }
        }
    }
    Vec::new()
}

fn similarity(a: &str, b: &str) -> f64 {
    if a.is_empty() && b.is_empty() {
        return 1.0;
    }
    
    let diff = TextDiff::from_words(a, b);
    let changes = diff.iter_all_changes().count();
    let total = a.split_whitespace().count() + b.split_whitespace().count();
    
    if total == 0 {
        return 0.0;
    }
    
    let same = total.saturating_sub(changes) as f64;
    (same * 2.0) / total as f64
}

fn find_duplicates(threshold: f64) -> Vec<(usize, usize, f64)> {
    let news = load_news();
    let mut duplicates: Vec<(usize, usize, f64)> = Vec::new();
    
    for i in 0..news.len() {
        for j in (i + 1)..news.len() {
            let title_sim = similarity(&news[i].title, &news[j].title);
            let desc_sim = similarity(&news[i].description, &news[j].description);
            let avg_sim = (title_sim + desc_sim) / 2.0;
            
            if avg_sim >= threshold {
                duplicates.push((i, j, avg_sim));
            }
        }
    }
    
    duplicates.sort_by(|a, b| b.2.partial_cmp(&a.2).unwrap_or(std::cmp::Ordering::Equal));
    duplicates
}

fn remove_duplicates(threshold: f64) -> usize {
    let news = load_news();
    let mut seen: HashSet<String> = HashSet::new();
    let mut unique: Vec<NewsItem> = Vec::new();
    let mut removed = 0;
    
    for item in news {
        let key = item.title.to_lowercase();
        let words: Vec<&str> = key.split_whitespace().collect();
        let mut is_duplicate = false;
        
        for i in 0..words.len().saturating_sub(2) {
            let phrase = words[i..].join(" ");
            if seen.contains(&phrase) {
                is_duplicate = true;
                removed += 1;
                break;
            }
        }
        
        let first_words: String = words.iter().take(5).copied().collect::<Vec<_>>().join(" ");
        if !first_words.is_empty() {
            seen.insert(first_words);
        }
        
        if !is_duplicate {
            unique.push(item);
        }
    }
    
    let storage = Storage { news: unique };
    let json = serde_json::to_string_pretty(&storage).unwrap_or_default();
    std::fs::write("../data/news.json", json).ok();
    
    removed
}

fn main() {
    let args: Vec<String> = env::args().collect();
    
    let threshold = args.iter()
        .position(|a| a == "--threshold")
        .and_then(|i| args.get(i + 1))
        .and_then(|s| s.parse().ok())
        .unwrap_or(0.8);
    
    if args.iter().any(|a| a == "--remove") {
        let removed = remove_duplicates(threshold);
        println!("Removed {} duplicate articles", removed);
    } else {
        let duplicates = find_duplicates(threshold);
        
        if duplicates.is_empty() {
            println!("No duplicates found (threshold: {})", threshold);
        } else {
            println!("Found {} duplicate pairs:\n", duplicates.len());
            for (i, j, score) in duplicates.iter().take(20) {
                println!("[{:.0}%] Article {} ~= Article {}", score * 100.0, i + 1, j + 1);
            }
            if duplicates.len() > 20 {
                println!("\n... and {} more", duplicates.len() - 20);
            }
        }
    }
}