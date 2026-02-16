//! Tanya Core - Binary entry point

use tanya_core::{init, Config, TanyaResult};

fn main() -> TanyaResult<()> {
    // Load configuration (could be from file, env, etc.)
    let config = Config {
        log_level: "info".to_string(),
        max_concurrent_tasks: 10,
        memory_limit_mb: 512,
    };
    
    // Initialize core
    init(config)?;
    
    println!("Tanya Core v0.1.0");
    println!("Type 'help' for available commands, 'quit' to exit.");
    
    // Simple REPL
    loop {
        print!("> ");
        std::io::Write::flush(&mut std::io::stdout()).ok();
        
        let mut input = String::new();
        if std::io::stdin().read_line(&mut input).ok() {
            let input = input.trim();
            
            match input {
                "quit" | "exit" => {
                    println!("Goodbye!");
                    break;
                }
                "help" => {
                    println!("Available commands:");
                    println!("  list - List available skills");
                    println!("  echo <text> - Echo text");
                    println!("  calc <expr> - Calculator (placeholder)");
                    println!("  quit - Exit");
                }
                "list" => {
                    // This would call into Rust skills
                    println!("[Rust Skills] echo, calculator");
                }
                cmd if cmd.starts_with("echo ") => {
                    let text = cmd.strip_prefix("echo ").unwrap_or("");
                    println!("Tanya says: {}", text);
                }
                cmd if cmd.starts_with("calc ") => {
                    println!("Calculator: {} (placeholder)", cmd.strip_prefix("calc ").unwrap_or(""));
                }
                "" => {}
                _ => {
                    println!("Unknown command. Type 'help' for available commands.");
                }
            }
        }
    }
    
    Ok(())
}
