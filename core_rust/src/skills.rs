//! Skills module - Fast skill execution in Rust

use serde::{Deserialize, Serialize};

/// Skill execution context
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SkillContext {
    pub action: String,
    pub params: serde_json::Value,
    pub orchestrator_state: Option<serde_json::Value>,
}

/// Skill execution result
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SkillResult {
    pub status: String,
    pub result: serde_json::Value,
    pub error: Option<String>,
}

impl SkillResult {
    pub fn success(result: serde_json::Value) -> Self {
        Self {
            status: "done".to_string(),
            result,
            error: None,
        }
    }
    
    pub fn error(msg: &str) -> Self {
        Self {
            status: "fail".to_string(),
            result: serde_json::Value::Null,
            error: Some(msg.to_string()),
        }
    }
}

/// Skill trait for implementing skills in Rust
pub trait Skill: Send + Sync {
    fn name(&self) -> &str;
    fn execute(&self, params: serde_json::Value) -> SkillResult;
}

/// Built-in skill: echo
pub struct EchoSkill;

impl Skill for EchoSkill {
    fn name(&self) -> &str {
        "echo"
    }
    
    fn execute(&self, params: serde_json::Value) -> SkillResult {
        let text = params.get("text")
            .and_then(|v| v.as_str())
            .unwrap_or("");
        SkillResult::success(serde_json::json!(format!("Tanya says: {}", text)))
    }
}

/// Built-in skill: calculator
pub struct CalculatorSkill;

impl Skill for CalculatorSkill {
    fn name(&self) -> &str {
        "calculator"
    }
    
    fn execute(&self, params: serde_json::Value) -> SkillResult {
        // Simple expression evaluator - can be extended
        let expr = params.get("expression")
            .and_then(|v| v.as_str())
            .unwrap_or("");
        
        // For now, just echo back - full eval needs more complex parsing
        SkillResult::success(serde_json::json!({
            "expression": expr,
            "note": "Calculator skill placeholder - implement expr crate for full eval"
        }))
    }
}

/// Skill registry for managing available skills
pub struct SkillRegistry {
    skills: Vec<Box<dyn Skill>>,
}

impl SkillRegistry {
    pub fn new() -> Self {
        let mut registry = Self { skills: Vec::new() };
        // Register built-in skills
        registry.register(Box::new(EchoSkill));
        registry.register(Box::new(CalculatorSkill));
        registry
    }
    
    pub fn register(&mut self, skill: Box<dyn Skill>) {
        self.skills.push(skill);
    }
    
    pub fn execute(&self, action: &str, params: serde_json::Value) -> SkillResult {
        for skill in &self.skills {
            if skill.name() == action {
                return skill.execute(params);
            }
        }
        SkillResult::error(&format!("No skill found for action: {}", action))
    }
    
    pub fn list_skills(&self) -> Vec<String> {
        self.skills.iter().map(|s| s.name().to_string()).collect()
    }
}

impl Default for SkillRegistry {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_echo_skill() {
        let skill = EchoSkill;
        let result = skill.execute(serde_json::json!({"text": "hello"}));
        assert_eq!(result.status, "done");
    }
    
    #[test]
    fn test_registry() {
        let registry = SkillRegistry::new();
        let result = registry.execute("echo", serde_json::json!({"text": "test"}));
        assert_eq!(result.status, "done");
    }
}
