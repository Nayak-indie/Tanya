//! Memory module - Fast memory operations in Rust

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::{Arc, RwLock};

/// A single memory entry
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MemoryEntry {
    pub key: String,
    pub value: serde_json::Value,
    pub timestamp: f64,
    pub metadata: Option<serde_json::Value>,
}

/// In-memory store for fast access
pub struct MemoryStore {
    entries: Arc<RwLock<HashMap<String, Vec<MemoryEntry>>>>,
}

impl MemoryStore {
    pub fn new() -> Self {
        Self {
            entries: Arc::new(RwLock::new(HashMap::new())),
        }
    }
    
    /// Store a value
    pub fn remember(&self, key: &str, value: serde_json::Value) {
        let entry = MemoryEntry {
            key: key.to_string(),
            value,
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .map(|d| d.as_secs_f64())
                .unwrap_or(0.0),
            metadata: None,
        };
        
        if let Ok(mut entries) = self.entries.write() {
            entries.entry(key.to_string()).or_insert_with(Vec::new).push(entry);
        }
    }
    
    /// Recall latest value for a key
    pub fn recall(&self, key: &str) -> Option<serde_json::Value> {
        if let Ok(entries) = self.entries.read() {
            if let Some(list) = entries.get(key) {
                return list.last().map(|e| e.value.clone());
            }
        }
        None
    }
    
    /// Recall all values for a key
    pub fn recall_all(&self, key: &str) -> Vec<serde_json::Value> {
        if let Ok(entries) = self.entries.read() {
            if let Some(list) = entries.get(key) {
                return list.iter().map(|e| e.value.clone()).collect();
            }
        }
        Vec::new()
    }
    
    /// Forget (clear) a key
    pub fn forget(&self, key: &str) {
        if let Ok(mut entries) = self.entries.write() {
            entries.remove(key);
        }
    }
    
    /// List all keys
    pub fn keys(&self) -> Vec<String> {
        if let Ok(entries) = self.entries.read() {
            entries.keys().cloned().collect()
        } else {
            Vec::new()
        }
    }
    
    /// Get count of entries
    pub fn len(&self) -> usize {
        if let Ok(entries) = self.entries.read() {
            entries.values().map(|v| v.len()).sum()
        } else {
            0
        }
    }
}

impl Default for MemoryStore {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_memory_remember_recall() {
        let memory = MemoryStore::new();
        memory.remember("test", serde_json::json!("value"));
        assert_eq!(memory.recall("test"), Some(serde_json::json!("value")));
    }
    
    #[test]
    fn test_memory_forget() {
        let memory = MemoryStore::new();
        memory.remember("test", serde_json::json!("value"));
        memory.forget("test");
        assert_eq!(memory.recall("test"), None);
    }
}
