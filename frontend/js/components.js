// Tanya Frontend - Interactive UI Components (JavaScript)

// Theme toggle functionality
const ThemeManager = {
    current: 'light',
    
    init() {
        const saved = localStorage.getItem('tanya-theme');
        if (saved) this.set(saved);
    },
    
    set(theme) {
        this.current = theme;
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('tanya-theme', theme);
        this.updateIcon();
    },
    
    toggle() {
        this.set(this.current === 'light' ? 'dark' : 'light');
    },
    
    updateIcon() {
        const icon = document.querySelector('#theme-toggle');
        if (icon) icon.textContent = this.current === 'light' ? '🌙' : '☀️';
    }
};

// Article card component
class ArticleCard {
    constructor(article) {
        this.article = article;
    }
    
    render() {
        const sentimentClass = this.article.sentiment === 'positive' ? 'sentiment-pos' :
                              this.article.sentiment === 'negative' ? 'sentiment-neg' : 'sentiment-neu';
        
        return `
            <div class="article-card" data-id="${this.article.id}">
                <div class="article-header">
                    <h3>${this.escape(this.article.title)}</h3>
                    <button class="favorite-btn" onclick="toggleFavorite('${this.article.id}')">
                        ${this.article.is_favorite ? '★' : '☆'}
                    </button>
                </div>
                <div class="article-meta">
                    <span class="sentiment-badge ${sentimentClass}">${this.article.sentiment}</span>
                    <span class="reading-time">${this.article.reading_time || 5} min read</span>
                    <span class="date">${this.formatDate(this.article.published)}</span>
                </div>
                <p class="article-summary">${this.escape(this.article.content?.substring(0, 200) || '')}...</p>
                <div class="article-actions">
                    <button onclick="shareArticle('${this.article.id}', 'twitter')">🐦</button>
                    <button onclick="shareArticle('${this.article.id}', 'linkedin')">💼</button>
                    <button onclick="openReaderMode('${this.article.id}')">📖</button>
                    <a href="${this.escape(this.article.link)}" target="_blank" class="original-link">Original ↗</a>
                </div>
            </div>
        `;
    }
    
    escape(str) {
        if (!str) return '';
        return str.replace(/[&<>"']/g, c => ({
            '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
        })[c]);
    }
    
    formatDate(date) {
        if (!date) return '';
        return new Date(date).toLocaleDateString();
    }
}

// Search component
class SearchBox {
    constructor(onSearch) {
        this.onSearch = onSearch;
        this.debounceTimer = null;
    }
    
    render() {
        return `
            <div class="search-box">
                <input type="text" id="search-input" 
                       placeholder="Search articles..."
                       oninput="handleSearch(this.value)">
                <select id="filter-sentiment">
                    <option value="">All Sentiments</option>
                    <option value="positive">Positive</option>
                    <option value="neutral">Neutral</option>
                    <option value="negative">Negative</option>
                </select>
            </div>
        `;
    }
    
    handleInput(value) {
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(() => {
            this.onSearch(value);
        }, 300);
    }
}

// Export functionality
const ExportManager = {
    async toJSON(articles) {
        const data = JSON.stringify(articles, null, 2);
        this.download(data, 'articles.json', 'application/json');
    },
    
    async toCSV(articles) {
        const headers = ['id', 'title', 'link', 'published', 'sentiment', 'reading_time'];
        const rows = articles.map(a => headers.map(h => this.escapeCSV(a[h] || '')));
        const csv = [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
        this.download(csv, 'articles.csv', 'text/csv');
    },
    
    download(content, filename, type) {
        const blob = new Blob([content], { type });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        URL.revokeObjectURL(url);
    },
    
    escapeCSV(str) {
        if (str.includes(',') || str.includes('"') || str.includes('\n')) {
            return `"${str.replace(/"/g, '""')}"`;
        }
        return str;
    }
};

// Share functionality
async function shareArticle(id, platform) {
    const article = await getArticle(id);
    const url = encodeURIComponent(article.link);
    const text = encodeURIComponent(article.title);
    
    const urls = {
        twitter: `https://twitter.com/intent/tweet?text=${text}&url=${url}`,
        linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${url}`
    };
    
    window.open(urls[platform], '_blank', 'width=600,height=400');
}

// Reader mode
function openReaderMode(articleId) {
    const modal = document.createElement('div');
    modal.className = 'reader-mode';
    modal.id = 'reader-modal';
    modal.innerHTML = `
        <div class="reader-content">
            <button class="close-btn" onclick="closeReaderMode()">✕</button>
            <div class="reader-text"></div>
        </div>
    `;
    document.body.appendChild(modal);
    
    // Load article content
    fetch(`/api/articles/${articleId}`)
        .then(r => r.json())
        .then(article => {
            document.querySelector('.reader-text').innerHTML = `
                <h1>${article.title}</h1>
                <p class="meta">${article.published} • ${article.reading_time} min read</p>
                <div class="content">${article.content}</div>
            `;
        });
}

function closeReaderMode() {
    const modal = document.getElementById('reader-modal');
    if (modal) modal.remove();
}

// Notifications
class NotificationManager {
    constructor() {
        this.permissions = null;
    }
    
    async init() {
        if ('Notification' in window) {
            this.permissions = Notification.permission;
        }
    }
    
    async requestPermission() {
        if ('Notification' in window) {
            this.permissions = await Notification.requestPermission();
            return this.permissions === 'granted';
        }
        return false;
    }
    
    notify(title, body, icon = '📰') {
        if (this.permissions === 'granted') {
            new Notification(title, { body, icon });
        }
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    ThemeManager.init();
    window.notifier = new NotificationManager();
});

export { ThemeManager, ArticleCard, SearchBox, ExportManager, NotificationManager };
