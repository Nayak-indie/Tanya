/**
 * Tanya RSS Scraper - Node.js
 * Run: node js/src/scraper.js [--source NAME] [--category CAT]
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const DATA_DIR = path.join(__dirname, '..', 'data');
const NEWS_FILE = path.join(DATA_DIR, 'news.json');
const SOURCES_FILE = path.join(DATA_DIR, 'sources.json');

// Default sources
const DEFAULT_SOURCES = [
  { name: 'BBC World', url: 'http://feeds.bbci.co.uk/news/world/rss.xml', category: 'World', enabled: true },
  { name: 'TechCrunch', url: 'https://techcrunch.com/feed/', category: 'Tech', enabled: true },
  { name: 'Hacker News', url: 'https://hnrss.org/frontpage', category: 'Tech', enabled: true },
  { name: 'Reuters', url: 'https://www.reutersagency.com/feed/', category: 'World', enabled: true },
];

// Fetch URL
function fetchURL(url) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    client.get(url, { timeout: 10000 }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

// Parse RSS (simple regex-based)
function parseRSS(xml, sourceName) {
  const items = [];
  const itemRegex = /<item>([\s\S]*?)<\/item>/gi;
  let match;
  
  while ((match = itemRegex.exec(xml)) !== null) {
    const itemXml = match[1];
    
    const title = extractTag(itemXml, 'title');
    const link = extractTag(itemXml, 'link');
    const desc = extractTag(itemXml, 'description');
    const pubDate = extractTag(itemXml, 'pubDate');
    
    if (title) {
      items.push({
        title: cleanHTML(title),
        link: link || '',
        description: cleanHTML(desc || '').substring(0, 500),
        pub_date: pubDate || new Date().toISOString(),
        source: sourceName,
        category: inferCategory(title + ' ' + desc),
        reading_time: estimateReadingTime(desc || ''),
        sentiment: analyzeSentiment(title + ' ' + desc),
        keywords: extractKeywords(title + ' ' + desc),
      });
    }
  }
  
  return items;
}

function extractTag(xml, tag) {
  const regex = new RegExp(`<${tag}[^>]*>([\\s\\S]*?)</${tag}>`, 'i');
  const match = xml.match(regex);
  return match ? match[1].trim() : null;
}

function cleanHTML(html) {
  return html
    .replace(/<[^>]+>/g, '')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .trim();
}

function estimateReadingTime(text) {
  const words = text.split(/\s+/).length;
  return Math.max(1, Math.ceil(words / 200));
}

function analyzeSentiment(text) {
  const lower = text.toLower();
  const positive = ['good', 'great', 'excellent', 'amazing', 'breakthrough', 'success', 'win'];
  const negative = ['bad', 'terrible', 'crisis', 'fail', 'death', 'war', 'attack', 'disaster'];
  
  const posCount = positive.filter(w => lower.includes(w)).length;
  const negCount = negative.filter(w => lower.includes(w)).length;
  
  if (posCount > negCount) return 'positive';
  if (negCount > posCount) return 'negative';
  return 'neutral';
}

function extractKeywords(text) {
  const stopWords = new Set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had']);
  
  const words = text.toLowerCase()
    .split(/\W+/)
    .filter(w => w.length > 3 && !stopWords.has(w));
  
  const freq = {};
  words.forEach(w => freq[w] = (freq[w] || 0) + 1);
  
  return Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([w]) => w);
}

function inferCategory(text) {
  const lower = text.toLowerCase();
  if (lower.includes('ai') || lower.includes('artificial intelligence')) return 'AI';
  if (lower.includes('tech') || lower.includes('software')) return 'Tech';
  if (lower.includes('stock') || lower.includes('market') || lower.includes('crypto')) return 'Finance';
  if (lower.includes('climate') || lower.includes('weather')) return 'Weather';
  if (lower.includes('war') || lower.includes('military')) return 'World';
  if (lower.includes('science') || lower.includes('space')) return 'Science';
  return 'General';
}

// Load existing news
function loadNews() {
  try {
    if (fs.existsSync(NEWS_FILE)) {
      return JSON.parse(fs.readFileSync(NEWS_FILE, 'utf8'));
    }
  } catch (e) {
    console.error('Error loading news:', e.message);
  }
  return [];
}

// Save news
function saveNews(news) {
  fs.writeFileSync(NEWS_FILE, JSON.stringify(news, null, 2));
  console.log(`Saved ${news.length} articles to ${NEWS_FILE}`);
}

// Fetch single source
async function fetchSource(source) {
  console.log(`Fetching ${source.name}...`);
  try {
    const xml = await fetchURL(source.url);
    const items = parseRSS(xml, source.name);
    console.log(`  -> Got ${items.length} items`);
    return items;
  } catch (e) {
    console.error(`  -> Error: ${e.message}`);
    return [];
  }
}

// Fetch all sources
async function fetchAll() {
  const sources = DEFAULT_SOURCES.filter(s => s.enabled);
  const allNews = [];
  
  for (const source of sources) {
    const items = await fetchSource(source);
    allNews.push(...items);
  }
  
  // Deduplicate by title
  const seen = new Set();
  const unique = allNews.filter(item => {
    const key = item.title.toLowerCase().substring(0, 50);
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
  
  saveNews(unique);
  console.log(`\nTotal: ${unique.length} unique articles`);
  return unique;
}

// CLI
const args = process.argv.slice(2);
if (args.includes('--help')) {
  console.log(`
Tanya RSS Scraper (Node.js)
===========================
Usage: node scraper.js [options]

Options:
  --all         Fetch all sources (default)
  --source N    Fetch specific source by name
  --category C  Filter by category
  --help        Show this help

Examples:
  node scraper.js --all
  node scraper.js --source BBC
  `);
  process.exit(0);
}

fetchAll().catch(console.error);
