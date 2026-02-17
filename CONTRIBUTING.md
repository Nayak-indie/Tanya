# Contributing to Tanya

Tanya is a polyglot experiment in building a news aggregator. We welcome contributions—whether it's fixing bugs, adding features, or improving documentation!

---

## Ways to Contribute

- 🐛 **Report bugs**
- 💡 **Suggest features**
- 📖 **Improve docs**
- 🔧 **Submit PRs**
- 🎨 **UI/UX improvements**

---

## Getting Started

```bash
# Fork & clone
git clone https://github.com/Nayak-indie/Tanya.git
cd Tanya

# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
streamlit run app.py
```

---

## Code Standards

- Follow PEP 8 for Python
- Add docstrings to new functions
- Keep functions small and focused

---

## Submitting PRs

1. Create a branch: `feature/your-feature`
2. Make changes
3. Test locally
4. Submit PR with clear description

---

## Project Structure

```
Tanya/
├── app.py              # Main UI
├── collect/            # RSS & HTML scrapers
├── backend/ml/         # Sentiment & analysis
├── core/              # Multi-lang engines
└── integrations/       # APIs & notifications
```

---

## Need Help?

Open an issue on GitHub!
