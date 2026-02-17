// Tanya - Database Operations (SQL)
// PostgreSQL/MySQL compatible schema

-- Articles table
CREATE TABLE IF NOT EXISTS articles (
    id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
    title VARCHAR(500) NOT NULL,
    link VARCHAR(2048) UNIQUE NOT NULL,
    content TEXT,
    published TIMESTAMP,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sentiment VARCHAR(20) DEFAULT 'neutral',
    reading_time INTEGER DEFAULT 5,
    keywords JSONB,
    is_favorite BOOLEAN DEFAULT FALSE,
    category VARCHAR(100),
    source VARCHAR(100),
    INDEX idx_published (published),
    INDEX idx_sentiment (sentiment),
    INDEX idx_favorite (is_favorite),
    FULLTEXT INDEX idx_content (title, content)
);

-- Keywords table for fast lookup
CREATE TABLE IF NOT EXISTS keywords (
    id SERIAL PRIMARY KEY,
    article_id VARCHAR(36) REFERENCES articles(id) ON DELETE CASCADE,
    keyword VARCHAR(100) NOT NULL,
    frequency INTEGER DEFAULT 1,
    UNIQUE(article_id, keyword)
);

CREATE INDEX idx_keywords_keyword ON keywords(keyword);

-- Search history
CREATE TABLE IF NOT EXISTS search_history (
    id SERIAL PRIMARY KEY,
    query VARCHAR(500) NOT NULL,
    results_count INTEGER,
    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id VARCHAR(36)
);

-- User preferences
CREATE TABLE IF NOT EXISTS user_preferences (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(36) UNIQUE,
    theme VARCHAR(20) DEFAULT 'light',
    notify_keywords TEXT[],
    notify_email VARCHAR(255),
    rss_feeds TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Collection history
CREATE TABLE IF NOT EXISTS collection_history (
    id SERIAL PRIMARY KEY,
    source VARCHAR(100) NOT NULL,
    articles_collected INTEGER,
    duplicates_found INTEGER,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Views
CREATE OR REPLACE VIEW articles_with_keywords AS
SELECT 
    a.*,
    COALESCE(
        json_agg(DISTINCT k.keyword) FILTER (WHERE k.keyword IS NOT NULL),
        '[]'::json
    ) as keywords_array
FROM articles a
LEFT JOIN keywords k ON a.id = k.article_id
GROUP BY a.id;

CREATE OR REPLACE VIEW daily_sentiment_summary AS
SELECT 
    DATE(published) as date,
    sentiment,
    COUNT(*) as count,
    AVG(reading_time) as avg_reading_time
FROM articles
WHERE published IS NOT NULL
GROUP BY DATE(published), sentiment
ORDER BY date DESC;

-- Stored procedures
CREATE OR REPLACE FUNCTION search_articles(query_text TEXT, limit_count INT DEFAULT 50)
RETURNS TABLE(
    id VARCHAR(36),
    title VARCHAR(500),
    link VARCHAR(2048),
    published TIMESTAMP,
    sentiment VARCHAR(20),
    reading_time INTEGER,
    similarity_score FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        a.id,
        a.title,
        a.link,
        a.published,
        a.sentiment,
        a.reading_time,
        ts_rank(to_tsvector('english', a.title || ' ' || COALESCE(a.content, '')), 
                plainto_tsquery('english', query_text)) as similarity_score
    FROM articles a
    WHERE to_tsvector('english', a.title || ' ' || COALESCE(a.content, '')) 
          @@ plainto_tsquery('english', query_text)
    ORDER BY similarity_score DESC
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql;

-- Trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER user_prefs_updated
    BEFORE UPDATE ON user_preferences
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

-- Sample queries
-- Get articles by keyword
-- SELECT * FROM articles_with_keywords 
-- WHERE 'AI' = ANY(keywords_array);

-- Search with ranking
-- SELECT * FROM search_articles('artificial intelligence', 10);

-- Daily sentiment trend
-- SELECT * FROM daily_sentiment_summary LIMIT 30;
