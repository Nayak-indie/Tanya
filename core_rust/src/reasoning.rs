//! Reasoning module - Structured reasoning primitives

use serde::{Deserialize, Serialize};

/// A reasoning step
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ReasoningStep {
    pub step: usize,
    pub thought: String,
    pub action: Option<String>,
    pub result: Option<String>,
}

/// A complete reasoning chain
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ReasoningChain {
    pub goal: String,
    pub steps: Vec<ReasoningStep>,
    pub final_result: Option<String>,
}

impl ReasoningChain {
    pub fn new(goal: &str) -> Self {
        Self {
            goal: goal.to_string(),
            steps: Vec::new(),
            final_result: None,
        }
    }
    
    pub fn add_step(&mut self, thought: &str, action: Option<&str>, result: Option<&str>) {
        self.steps.push(ReasoningStep {
            step: self.steps.len() + 1,
            thought: thought.to_string(),
            action: action.map(String::from),
            result: result.map(String::from),
        });
    }
    
    pub fn finish(&mut self, result: &str) {
        self.final_result = Some(result.to_string());
    }
    
    pub fn is_complete(&self) -> bool {
        self.final_result.is_some()
    }
    
    pub fn to_prompt(&self) -> String {
        let mut prompt = format!("Goal: {}\n\n", self.goal);
        for step in &self.steps {
            prompt += &format!("{}. {}\n", step.step, step.thought);
            if let Some(ref action) = step.action {
                prompt += &format!("   Action: {}\n", action);
            }
            if let Some(ref result) = step.result {
                prompt += &format!("   Result: {}\n", result);
            }
        }
        if let Some(ref result) = self.final_result {
            prompt += &format!("\nFinal: {}", result);
        }
        prompt
    }
}

/// Intent classification
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum Intent {
    Question,
    Command,
    Statement,
    Greeting,
    Goodbye,
    Unknown,
}

impl Intent {
    pub fn classify(text: &str) -> Self {
        let lower = text.to_lowercase();
        
        // Greeting patterns
        if lower.starts_with("hello") || lower.starts_with("hi") || 
           lower.starts_with("hey") || lower.starts_with("greetings") {
            return Intent::Greeting;
        }
        
        // Goodbye patterns
        if lower.contains("bye") || lower.contains("goodbye") || 
           lower.contains("see you") {
            return Intent::Goodbye;
        }
        
        // Command patterns (starts with verb or explicit command words)
        if lower.starts_with("run ") || lower.starts_with("execute ") ||
           lower.starts_with("do ") || lower.starts_with("make ") ||
           lower.starts_with("create ") || lower.starts_with("delete ") ||
           lower.starts_with("list ") || lower.starts_with("show ") {
            return Intent::Command;
        }
        
        // Question patterns
        if lower.ends_with("?") || lower.starts_with("what") || 
           lower.starts_with("how") || lower.starts_with("why") ||
           lower.starts_with("when") || lower.starts_with("where") ||
           lower.starts_with("who") || lower.starts_with("which") {
            return Intent::Question;
        }
        
        // Default to statement
        Intent::Statement
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_reasoning_chain() {
        let mut chain = ReasoningChain::new("Test goal");
        chain.add_step("First thought", Some("do_something"), Some("success"));
        chain.finish("Done");
        
        assert!(chain.is_complete());
        assert_eq!(chain.steps.len(), 1);
    }
    
    #[test]
    fn test_intent_classify() {
        assert_eq!(Intent::classify("Hello there"), Intent::Greeting);
        assert_eq!(Intent::classify("What is this?"), Intent::Question);
        assert_eq!(Intent::classify("Run my command"), Intent::Command);
    }
}
