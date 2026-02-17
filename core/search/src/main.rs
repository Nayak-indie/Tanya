//! Tanya - Full-Text Search Engine (Rust)
//! High-performance fuzzy search using TF-IDF and BM25

use std::collections::HashMap;
use std::fs::File;
use std::io::{BufReader, BufWriter, Write};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Article {
    pub id: String,
    pub title: String,
    pub link: String,
    pub content: String,
    pub keywords: Vec<String>,
    pub published: String,
}

#[derive(Debug, Clone)]
pub struct SearchResult {
    pub article_id: String,
    pub score: f64,
    pub matches: Vec<String>,
}

pub struct SearchEngine {
    documents: HashMap<String, Article>,
    inverted_index: HashMap<String, Vec<String>>, // word -> doc IDs
    doc_lengths: HashMap<String, usize>,
    avg_doc_length: f64,
    total_docs: usize,
}

impl SearchEngine {
    pub fn new() -> Self {
        SearchEngine {
            documents: HashMap::new(),
            inverted_index: HashMap::new(),
            doc_lengths: HashMap::new(),
            avg_doc_length: 0.0,
            total_docs: 0,
        }
    }

    pub fn add_document(&mut self, article: Article) {
        let id = article.id.clone();
        let length = self.tokenize(&article.title).len() + self.tokenize(&article.content).len();
        
        self.documents.insert(id.clone(), article);
        self.doc_lengths.insert(id.clone(), length);
        
        for word in self.tokenize(&self.documents[&id].title) {
            self.inverted_index.entry(word).or_insert_with(Vec::new).push(id.clone());
        }
        for word in self.tokenize(&self.documents[&id].content) {
            self.inverted_index.entry(word).or_insert_with(Vec::new).push(id.clone());
        }
        
        self.total_docs = self.documents.len();
        let total_len: usize = self.doc_lengths.values().sum();
        self.avg_doc_length = total_len as f64 / self.total_docs as f64;
    }

    fn tokenize(&self, text: &str) -> Vec<String> {
        text.to_lowercase()
            .split(|c: char| !c.is_alphanumeric())
            .filter(|s| s.len() > 2)
            .map(|s| s.to_string())
            .collect()
    }

    // BM25 ranking algorithm
    pub fn search(&self, query: &str, limit: usize) -> Vec<SearchResult> {
        let query_terms = self.tokenize(query);
        let mut scores: HashMap<String, f64> = HashMap::new();
        let k1 = 1.5;
        let b = 0.75;

        for term in &query_terms {
            if let Some(doc_ids) = self.inverted_index.get(term) {
                let idf = ((self.total_docs as f64 - doc_ids.len() as f64 + 0.5) / 
                          (doc_ids.len() as f64 + 0.5) + 1.0).ln();
                
                for doc_id in doc_ids {
                    let doc_len = *self.doc_lengths.get(doc_id).unwrap_or(&1);
                    let tf = 1.0; // Simplified term frequency
                    let score = idf * (tf * (k1 + 1.0)) / 
                               (tf + k1 * (1.0 - b + b * (doc_len as f64 / self.avg_doc_length)));
                    *scores.entry(doc_id.clone()).or_insert(0.0) += score;
                }
            }
        }

        let mut results: Vec<SearchResult> = scores
            .into_iter()
            .map(|(id, score)| SearchResult {
                article_id: id,
                score,
                matches: query_terms.clone(),
            })
            .collect();
        
        results.sort_by(|a, b| b.score.partial_cmp(&a.score).unwrap());
        results.truncate(limit);
        results
    }

    pub fn fuzzy_search(&self, query: &str, limit: usize) -> Vec<SearchResult> {
        let query_terms = self.tokenize(query);
        let mut results: Vec<SearchResult> = Vec::new();

        for (id, doc) in &self.documents {
            let mut score = 0.0;
            let mut matches = Vec::new();
            
            let doc_text = format!("{} {}", doc.title, doc.content).to_lowercase();
            
            for term in &query_terms {
                if doc_text.contains(term) {
                    score += 1.0;
                    matches.push(term.clone());
                } else {
                    // Fuzzy matching - allow 1-2 character differences
                    for word in doc_text.split_whitespace() {
                        if self.levenshtein_distance(term, word) <= 2 {
                            score += 0.5;
                            matches.push(term.clone());
                            break;
                        }
                    }
                }
            }
            
            if score > 0.0 {
                results.push(SearchResult {
                    article_id: id.clone(),
                    score,
                    matches,
                });
            }
        }

        results.sort_by(|a, b| b.score.partial_cmp(&a.score).unwrap());
        results.truncate(limit);
        results
    }

    fn levenshtein_distance(&self, s1: &str, s2: &str) -> usize {
        let (m, n) = (s1.len(), s2.len());
        if m == 0 return n;
        if n == 0 return m;

        let mut matrix = vec![vec![0usize; n + 1]; m + 1];
        
        for i in 0..=m { matrix[i][0] = i; }
        for j in 0..=n { matrix[0][j] = j; }

        for i in 1..=m {
            for j in 1..=n {
                let cost = if s1.chars().nth(i-1) == s2.chars().nth(j-1) { 0 } else { 1 };
                matrix[i][j] = std::cmp::min(
                    std::cmp::min(matrix[i-1][j] + 1, matrix[i][j-1] + 1),
                    matrix[i-1][j-1] + cost
                );
            }
        }
        matrix[m][n]
    }

    pub fn save_index(&self, path: &str) -> std::io::Result<()> {
        let file = File::create(path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer(writer, &self.documents).unwrap();
        Ok(())
    }

    pub fn load_index(&mut self, path: &str) -> std::io::Result<()> {
        let file = File::open(path)?;
        let reader = BufReader::new(file);
        self.documents = serde_json::from_reader(reader).unwrap();
        Ok(())
    }
}

fn main() {
    let mut engine = SearchEngine::new();
    
    engine.add_document(Article {
        id: "1".to_string(),
        title: "AI Breakthrough in 2026".to_string(),
        link: "https://example.com/ai".to_string(),
        content: "New artificial intelligence research shows breakthrough".to_string(),
        keywords: vec!["AI".to_string(), "research".to_string()],
        published: "2026-02-17".to_string(),
    });

    let results = engine.search("AI research", 5);
    for r in results {
        println!("ID: {}, Score: {:.2}", r.article_id, r.score);
    }
}
