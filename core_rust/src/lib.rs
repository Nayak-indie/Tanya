//! Tanya Core - Rust Backend Library
//! 
//! Provides performance-critical functionality for the Tanya AI agent framework.
//! - Fast skill execution
//! - Memory management
//! - Structured reasoning primitives

pub mod skills;
pub mod memory;
pub mod reasoning;

use serde::{Deserialize, Serialize};

/// Result type for Tanya core operations
pub type TanyaResult<T> = Result<T, TanyaError>;

/// Core error types
#[derive(Debug, thiserror::Error)]
pub enum TanyaError {
    #[error("Skill execution failed: {0}")]
    SkillError(String),
    
    #[error("Memory error: {0}")]
    MemoryError(String),
    
    #[error("Serialization error: {0}")]
    SerializationError(#[from] serde_json::Error),
    
    #[error("IO error: {0}")]
    IoError(#[from] std::io::Error),
}

/// Core configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Config {
    pub log_level: String,
    pub max_concurrent_tasks: usize,
    pub memory_limit_mb: usize,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            log_level: "info".to_string(),
            max_concurrent_tasks: 10,
            memory_limit_mb: 512,
        }
    }
}

/// Initialize the core with configuration
pub fn init(config: Config) -> TanyaResult<()> {
    env_logger::Builder::from_env(
        env_logger::Env::default().default_filter_or(&config.log_level)
    ).init();
    
    log::info!("Tanya Core initialized");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_default_config() {
        let config = Config::default();
        assert_eq!(config.log_level, "info");
    }
}
