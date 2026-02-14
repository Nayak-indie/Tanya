# Contributing to Tanya 🤝

First off, thank you for considering contributing to Tanya! This project is in active development and we need your help to make it better.

## 🚧 Current State

This repository is undergoing major restructuring. We're being transparent: things are messy right now, but that makes it a **great opportunity** for meaningful contributions that will shape the project's future.

## 🎯 How Can I Contribute?

### Reporting Bugs
- **Check existing issues** first to avoid duplicates
- **Use the bug report template** when creating issues
- Include: OS, Python version, steps to reproduce, expected vs actual behavior
- Add relevant logs or screenshots

### Suggesting Enhancements
- **Check if it's already planned** in existing issues
- Explain **why** this enhancement would be useful
- Provide examples of how it would work

### Code Contributions

#### Good First Issues
Look for issues labeled `good first issue` - these are perfect for newcomers:
- Documentation improvements
- Adding code comments
- Fixing small bugs
- Improving error messages

#### Before You Start
1. **Comment on the issue** you want to work on
2. Wait for confirmation to avoid duplicate work
3. Ask questions if anything is unclear

## 🔧 Development Setup

### Prerequisites
- Python 3.8+
- Git
- pip

### Setup Steps
```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/Tanya.git
cd Tanya

# 3. Add upstream remote
git remote add upstream https://github.com/Nayak-indie/Tanya.git

# 4. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Create a branch for your work
git checkout -b feature/your-feature-name
```

## 📝 Code Style & Standards

### Python Guidelines
- Follow **PEP 8** style guide
- Use **type hints** where possible
- Write **docstrings** for functions and classes
- Keep functions **small and focused**

### Example
```python
def process_message(message: str, context: dict) -> str:
    """
    Process user message and return AI response.
    
    Args:
        message: User input text
        context: Conversation context dictionary
        
    Returns:
        AI-generated response string
    """
    # Your code here
    pass
```

### Commit Messages
Write clear, descriptive commit messages:

**Good:**
```
Add support for context memory in chat
Fix bug in message preprocessing
Update README with installation steps
```

**Bad:**
```
update
fix stuff
changes
```

### Commit Message Format
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Example:**
```
feat: Add memory persistence to chat history

Implements SQLite database to store conversation history
across sessions. Includes migration script for existing users.

Closes #42
```

## 🔄 Pull Request Process

### Before Submitting
- [ ] Code follows the style guidelines
- [ ] Self-review of your code
- [ ] Commented complex/hard-to-understand areas
- [ ] Updated documentation if needed
- [ ] No unnecessary files (logs, model files, cache)
- [ ] Tested your changes locally

### Submitting PR
1. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request** on GitHub
   - Use a clear, descriptive title
   - Reference related issues (e.g., "Fixes #123")
   - Explain what and why (not how - code shows how)
   - Add screenshots/demos if applicable

3. **PR Template** (use this structure):
   ```markdown
   ## Description
   Brief description of changes
   
   ## Related Issue
   Closes #123
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Refactoring
   
   ## Testing
   How did you test this?
   
   ## Screenshots (if applicable)
   ```

4. **Respond to feedback** promptly and be open to suggestions

### Review Process
- Maintainers will review your PR within 3-5 days
- You may be asked to make changes
- Once approved, maintainers will merge your PR

## 📁 Project Structure (Target)

We're working towards this structure:
```
Tanya/
├── tanya/              # Main package
│   ├── core/           # Core functionality
│   ├── brain/          # AI/ML components
│   ├── tools/          # Utility tools
│   └── api/            # API interfaces
├── tests/              # Test files
├── docs/               # Documentation
├── examples/           # Usage examples
├── scripts/            # Utility scripts
└── requirements.txt
```

## 🧪 Testing

### Running Tests
```bash
# Once we have tests set up
pytest tests/
```

### Writing Tests
- Add tests for new features
- Test edge cases and error conditions
- Aim for good coverage (we'll add coverage tools later)

## 🐛 Debugging Tips

### Common Issues
1. **Import errors**: Check your virtual environment is activated
2. **Model files**: These are ignored - download separately if needed
3. **Path issues**: Use absolute imports within the package

### Getting Help
- Comment on the relevant issue
- Join discussions in existing PRs
- Be specific about what you've tried

## 📚 Resources

### Learning Resources
- [Python PEP 8 Style Guide](https://pep8.org/)
- [How to Write Git Commit Messages](https://chris.beams.io/posts/git-commit/)
- [First Contributions Guide](https://github.com/firstcontributions/first-contributions)

### Project-Specific
- Check `README.md` for project overview
- See `TODO.md` for planned features
- Review existing issues for context

## 🎖️ Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Acknowledged in the README (for significant contributions)

## 💬 Questions?

- **Open an issue** with the `question` label
- **Start a discussion** in the Discussions tab (if enabled)
- **Comment on existing issues** for clarification

## 📜 Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive environment for everyone.

### Expected Behavior
- Be respectful and considerate
- Accept constructive criticism gracefully
- Focus on what's best for the project
- Show empathy towards other contributors

### Unacceptable Behavior
- Harassment or discriminatory comments
- Trolling or insulting remarks
- Public or private harassment
- Publishing others' private information

### Enforcement
Violations can be reported to project maintainers. We will review and investigate all complaints and respond appropriately.

---

## 🚀 Ready to Contribute?

1. Find an issue you want to work on
2. Comment to claim it
3. Fork, code, test
4. Submit a PR
5. Celebrate your contribution! 🎉

**Remember:** No contribution is too small. Documentation, typo fixes, code comments - it all matters!

Thank you for helping make Tanya better! 🙏