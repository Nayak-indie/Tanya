/**
 * NewsFlow Node.js Collector
 * Alternative collector using Node.js/TypeScript
 */
const Parser = require('rss-parser');
const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');
const path = require('path');

const parser = new Parser();

// Default RSS sources
const RSS_SOURCES = [
    { name: 'BBC News', url: 'https://feeds.bbci.co.uk/news/rss.xml', enabled: true },
    { name: 'TechCrunch', url: 'https://techcrunch.com/feed/', enabled: true },
    { name: 'Hacker News', url: 'https://news.ycombinator.com/rss', enabled: true },
    { name: 'Reuters', url: 'https://www.reutersagency.com/feed/', enabled: true },
];

const DATA_DIR = path.join(__dirname, '..', 'data');
const NEWS_FILE = path.join(DATA_DIR, 'news.json');

/**
 * Fetch RSS feed
 */
async function fetchRSS(source) {
    try {
        const feed = await parser.parseURL(source.url);
        return feed.items.map(item => ({
            title: item.title || 'No Title',
            link: item.link || '',
            published: item.pubDate || item.isoDate || '',
            summary: (item.contentSnippet || item.content || '').substring(0, 200),
            source: source.name
        }));
    } catch (error) {
        console.error(`Error fetching ${source.name}:`, error.message);
        return [];
    }
}

/**
 * Fetch HTML page
 */
async function fetchHTML(url, sourceName) {
    try {
        const response = await axios.get(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            timeout: 10000
        });
        
        const $ = cheerio.load(response.data);
        const articles = [];
        
        // Try common selectors
        $('article h2, article h3, .headline, .news-title').each((i, el) => {
            if (i >= 20) return;
            const title = $(el).text().trim();
            const link = $(el).find('a').attr('href') || $(el).parent().attr('href') || '';
            
            if (title && title.length > 10) {
                articles.push({
                    title,
                    link: link.startsWith('http') ? link : url + link,
                    source: sourceName
                });
            }
        });
        
        return articles;
    } catch (error) {
        console.error(`Error fetching ${url}:`, error.message);
        return [];
    }
}

/**
 * Main collection function
 */
async function collect() {
    console.log('📰 NewsFlow Collector starting...');
    
    // Ensure data directory exists
    if (!fs.existsSync(DATA_DIR)) {
        fs.mkdirSync(DATA_DIR, { recursive: true });
    }
    
    const allNews = [];
    
    // Collect from RSS sources
    console.log('📡 Fetching RSS feeds...');
    for (const source of RSS_SOURCES) {
        if (source.enabled) {
            const articles = await fetchRSS(source);
            console.log(`  ✓ ${source.name}: ${articles.length} articles`);
            allNews.push(...articles);
        }
    }
    
    // Sort by date
    allNews.sort((a, b) => new Date(b.published) - new Date(a.published));
    
    // Save to file
    const data = {
        collected_at: new Date().toISOString(),
        articles: allNews
    };
    
    fs.writeFileSync(NEWS_FILE, JSON.stringify(data, null, 2));
    
    console.log(`\n✅ Collected ${allNews.length} articles total`);
    console.log(`💾 Saved to ${NEWS_FILE}`);
}

// Run if executed directly
if (require.main === module) {
    collect().catch(console.error);
}

module.exports = { collect, fetchRSS, fetchHTML };
