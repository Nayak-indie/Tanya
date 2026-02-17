/**
 * Tanya RSS Scraper - Kotlin
 * Build: kotlinc -include-runtime -d rss_scraper.jar rss_scraper.kt
 * Run: kotlin -classpath rss_scraper.jar RssScraperKt
 */

import java.net.HttpURLConnection
import java.net.URL
import java.io.BufferedReader
import java.io.InputStreamReader

data class RSSItem(
    val title: String,
    val link: String,
    val description: String,
    val source: String,
    val category: String,
    val sentiment: String,
    val readingTime: Int
)

data class FeedSource(
    val name: String,
    val url: String,
    val category: String
)

object RSSScraper {
    private val FEEDS = listOf(
        FeedSource("BBC", "http://feeds.bbci.co.uk/news/world/rss.xml", "World"),
        FeedSource("TechCrunch", "https://techcrunch.com/feed/", "Tech")
    )
    
    private val POSITIVE_WORDS = listOf("good", "great", "excellent", "amazing", "breakthrough", "success", "win")
    private val NEGATIVE_WORDS = listOf("bad", "terrible", "crisis", "fail", "death", "war", "attack", "disaster")
    private val STOP_WORDS = setOf("the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "from", "is", "are")
    
    fun fetch(url: String): String {
        val connection = URL(url).openConnection() as HttpURLConnection
        connection.setRequestProperty("User-Agent", "Tanya/1.0 RSS (Kotlin)")
        connection.connectTimeout = 10000
        connection.readTimeout = 10000
        
        val reader = BufferedReader(InputStreamReader(connection.inputStream))
        return reader.readText()
    }
    
    fun parse(xml: String, source: String): List<RSSItem> {
        val items = mutableListOf<RSSItem>()
        
        // Simple regex extraction
        val titleRegex = "<title>([^<]+)</title>".toRegex()
        val titles = titleRegex.findAll(xml).map { it.groupValues[1] }.drop(1)
        
        for (title in titles.take(20)) {
            val item = RSSItem(
                title = title,
                link = "",
                description = "",
                source = source,
                category = inferCategory(title),
                sentiment = analyzeSentiment(title),
                readingTime = estimateReadingTime(title)
            )
            items.add(item)
        }
        
        return items
    }
    
    fun analyzeSentiment(text: String): String {
        val lower = text.lowercase()
        val posCount = POSITIVE_WORDS.count { lower.contains(it) }
        val negCount = NEGATIVE_WORDS.count { lower.contains(it) }
        
        return when {
            posCount > negCount -> "positive"
            negCount > posCount -> "negative"
            else -> "neutral"
        }
    }
    
    fun inferCategory(text: String): String {
        val lower = text.lowercase()
        return when {
            lower.contains("ai") || lower.contains("artificial intelligence") -> "AI"
            lower.contains("tech") || lower.contains("software") -> "Tech"
            lower.contains("stock") || lower.contains("market") -> "Finance"
            lower.contains("war") || lower.contains("military") -> "World"
            lower.contains("science") || lower.contains("space") -> "Science"
            else -> "General"
        }
    }
    
    fun estimateReadingTime(text: String): Int {
        val wordCount = text.split(" ").size
        return maxOf(1, wordCount / 200)
    }
    
    fun extractKeywords(text: String): List<String> {
        val words = text.lowercase()
            .split(Regex("\\W+"))
            .filter { it.length > 3 && it !in STOP_WORDS }
        
        return words.groupingBy { it }.eachCount()
            .entries
            .sortedByDescending { it.value }
            .take(10)
            .map { it.key }
    }
    
    @JvmStatic
    fun main(args: Array<String>) {
        println("Tanya RSS Scraper (Kotlin)")
        println("===========================")
        println()
        
        val feedsToFetch = if (args.isNotEmpty() && args[0] == "--url") {
            listOf(FeedSource("Custom", args[1], "General"))
        } else {
            FEEDS
        }
        
        var totalItems = 0
        for (feed in feedsToFetch) {
            println("Fetching ${feed.name}...")
            try {
                val xml = fetch(feed.url)
                val items = parse(xml, feed.name)
                println("  -> Found ${items.size} articles")
                
                for (item in items.take(5)) {
                    println("    - ${item.title}")
                }
                
                totalItems += items.size
            } catch (e: Exception) {
                println("  -> Error: ${e.message}")
            }
        }
        
        println()
        println("Total: $totalItems articles")
        println("Engine: Kotlin (JVM, statically typed)")
    }
}
