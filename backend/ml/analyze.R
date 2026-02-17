# Tanya - Statistical Analysis Module (R)
# Trend analysis, sentiment distribution, keyword frequency

library(jsonlite)

# Configuration
CONFIG <- list(
  min_keyword_length = 4,
  top_n_keywords = 20,
  sentiment_weights = c(positive = 1, neutral = 0, negative = -1)
)

#' Load articles from JSON file
load_articles <- function(filepath = "data/news.json") {
  if (!file.exists(filepath)) {
    return(data.frame())
  }
  
  data <- fromJSON(filepath)
  
  if (is.list(data) && !is.null(data$articles)) {
    articles <- data$articles
  } else {
    articles <- as.data.frame(data)
  }
  
  return(articles)
}

#' Calculate sentiment distribution
sentiment_distribution <- function(articles) {
  if (nrow(articles) == 0) {
    return(data.frame(sentiment = character(), count = integer()))
  }
  
  # Ensure sentiment column exists
  if (!"sentiment" %in% colnames(articles)) {
    articles$sentiment <- "neutral"
  }
  
  dist <- table(articles$sentiment)
  as.data.frame(dist, stringsAsFactors = FALSE)
}

#' Keyword frequency analysis
keyword_frequency <- function(articles, top_n = 20) {
  if (nrow(articles) == 0) {
    return(data.frame(keyword = character(), count = integer()))
  }
  
  # Combine all text
  all_text <- paste(
    paste(articles$title, collapse = " "),
    paste(articles$content %||% "", collapse = " ")
  )
  
  # Tokenize and clean
  words <- tolower(unlist(strsplit(all_text, "\\W+")))
  words <- words[nchar(words) >= CONFIG$min_keyword_length]
  
  # Remove stopwords
  stopwords <- c("the", "and", "for", "are", "but", "not", "you", 
                "all", "can", "had", "her", "was", "one", "our",
                "out", "has", "have", "been", "were", "their")
  words <- words[!words %in% stopwords]
  
  # Count frequencies
  freq <- sort(table(words), decreasing = TRUE)
  
  top <- head(freq, top_n)
  data.frame(
    keyword = names(top),
    count = as.integer(top),
    stringsAsFactors = FALSE
  )
}

#' Trend analysis over time
trend_analysis <- function(articles) {
  if (nrow(articles) == 0 || is.null(articles$published)) {
    return(data.frame())
  }
  
  # Parse dates
  articles$date <- as.Date(articles$published, format = "%a, %d %b %Y %H:%M:%S", tz = "GMT")
  articles$date[is.na(articles$date)] <- Sys.Date()
  
  # Aggregate by date
  daily <- aggregate(
    list(count = rep(1, nrow(articles))), 
    by = list(date = format(articles$date, "%Y-%m-%d")),
    FUN = sum
  )
  
  daily <- daily[order(daily$date), ]
  
  # Calculate moving average
  if (nrow(daily) >= 7) {
    daily$ma7 <- stats::filter(daily$count, rep(1/7, 7), sides = 1)
  }
  
  return(daily)
}

#' Sentiment score over time
sentiment_trend <- function(articles) {
  if (nrow(articles) == 0 || is.null(articles$published)) {
    return(data.frame())
  }
  
  articles$date <- as.Date(articles$published, format = "%a, %d %b %Y %H:%M:%S", tz = "GMT")
  articles$date[is.na(articles$date)] <- Sys.Date()
  
  if (!"sentiment" %in% colnames(articles)) {
    articles$sentiment <- "neutral"
  }
  
  # Map sentiment to score
  articles$score <- sapply(articles$sentiment, function(s) {
    CONFIG$sentiment_weights[[s]] %||% 0
  })
  
  # Aggregate by date
  trend <- aggregate(
    list(
      avg_sentiment = articles$score,
      count = articles$score
    ),
    by = list(date = format(articles$date, "%Y-%m-%d")),
    FUN = mean
  )
  
  return(trend[order(trend$date), ])
}

#' Generate summary statistics
summary_stats <- function(articles) {
  if (nrow(articles) == 0) {
    return(list(
      total_articles = 0,
      date_range = c(NA, NA),
      avg_reading_time = NA,
      sentiment_breakdown = c()
    ))
  }
  
  list(
    total_articles = nrow(articles),
    date_range = range(articles$published, na.rm = TRUE),
    avg_reading_time = mean(articles$reading_time %||% 5, na.rm = TRUE),
    sentiment_breakdown = sentiment_distribution(articles)$Freq,
    top_keywords = head(keyword_frequency(articles, 10)$keyword, 10)
  )
}

#' Export to CSV
export_csv <- function(articles, filepath = "export.csv") {
  write.csv(articles, filepath, row.names = FALSE)
  cat("Exported", nrow(articles), "articles to", filepath, "\n")
}

# Demo
cat("=== Tanya R Analysis Module ===\n\n")

# Create sample data
sample_articles <- data.frame(
  id = 1:5,
  title = c("Great AI Breakthrough", "Market Crash Update", "Neutral News Report", 
            "Excellent Results", "Problem Discovered"),
  content = c("Amazing progress in AI technology", "Stocks fall dramatically",
              "Regular news update", "Outstanding performance", "Issue found in system"),
  published = c("Mon, 16 Feb 2026 10:00:00 GMT", "Mon, 16 Feb 2026 11:00:00 GMT",
               "Mon, 16 Feb 2026 12:00:00 GMT", "Mon, 16 Feb 2026 13:00:00 GMT",
               "Mon, 16 Feb 2026 14:00:00 GMT"),
  sentiment = c("positive", "negative", "neutral", "positive", "negative"),
  reading_time = c(5, 3, 4, 6, 2),
  stringsAsFactors = FALSE
)

cat("Sentiment Distribution:\n")
print(sentiment_distribution(sample_articles))

cat("\nKeyword Frequency:\n")
print(keyword_frequency(sample_articles, 5))

cat("\nTrend Analysis:\n")
print(trend_analysis(sample_articles))

cat("\nSummary:\n")
print(summary_stats(sample_articles))
