//! Search Engine - Full-text search using Rust
//! Build: cd rust && cargo build --release
//! Run:   ./target/release/search <query>

use serde::{Deserialize, Serialize};
use similar::{ChangeTag, TextDiff};
use std::collections::HashMap;
use std::env;
use std::fs;
use std::path::Path;

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct SearchResult {
    pub title: String,
    pub link: String,
    pub description: String,
    pub source: String,
    pub score: f64,
    pub category: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct NewsItem {
    title: String,
    link: String,
    description: String,
    source: String,
    category: String,
}

fn load_news() -> Vec<NewsItem> {
    let news_path = Path::new("../data/news.json");
    if let Ok(content) = fs::read_to_string(news_path) {
        if let Ok(news) = serde_json::from_str::<Vec<NewsItem>>(&content) {
            return news;
        }
    }
    Vec::new()
}

fn calculate_score(query: &str, item: &NewsItem) -> f64 {
    let query_lower = query.to_lowercase();
    let query_terms: Vec<&str> = query_lower.split_whitespace().collect();
    
    let mut score = 0.0;
    
    // Title matches (highest weight)
    let title_lower = item.title.to_lowercase();
    for term in &query_terms {
        if title_lower.contains(term) {
            score += 10.0;
            if title_lower.starts_with(term) {
                score += 5.0;
            }
        }
    }
    
    // Description matches
    let desc_lower = item.description.to_lowercase();
    for term in &query_terms {
        if desc_lower.contains(term) {
            score += 3.0;
        }
    }
    
    // Category match
    if query_lower == item.category.to_lowercase() {
        score += 5.0;
    }
    
    score
}

pub fn search(query: &str, limit: usize) -> Vec<SearchResult> {
    let news = load_news();
    let mut results: Vec<SearchResult> = news
        .into_iter()
        .map(|item| {
            let score = calculate_score(query, &item);
            SearchResult {
                title: item.title,
                link: item.link,
                description: item.description,
                source: item.source,
                score,
                category: item.category,
            }
        })
        .filter(|r| r.score > 0.0)
        .collect();
    
    results.sort_by(|a, b| b.score.partial_cmp(&a.score).unwrap_or(std::cmp::Ordering::Equal));
    results.truncate(limit);
    results
}

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 {
        println!("Tanya Search Engine (Rust)");
        println!("Usage: search <query> [--limit N]");
        println!("Example: search ai --limit 10");
        return;
    }
    
    let query = &args[1];
    let mut limit = 20;
    
    if let Some(pos) = args.iter().position(|a| a == "--limit") {
        if let Some(l) = args.get(pos + 1) {
            limit = l.parse().unwrap_or(20);
        }
    }
    
    let results = search(query, limit);
    
    for (i, result) in results.iter().enumerate() {
        println!("{}. [{}] {}", i + 1, result.category, result.title);
        println!("   Score: {:.1} | Source: {}", result.score, result.source);
        println!("   Link: {}", result.link);
        if !result.description.is_empty() {
            let desc = if result.description.len() > 150 {
                format!("{}...", &result.description[..150])
            } else {
                result.description.clone()
            };
            println!("   {}", desc);
        }
        println!();
    }
    
    if results.is_empty() {
        println!("No results found for '{}'", query);
    }
}