# Tanya RSS Analysis in Julia
# Run: julia julia/src/analyzer.jl [--url URL]
# Install: julia> import Pkg; Pkg.add("HTTP") Pkg.add("JSON")

using HTTP
using JSON
using Statistics

# Configuration
const CONFIG = Dict(
    :timeout => 30,
    :user_agent => "Tanya/1.0 RSS Analyzer (Julia)",
    :data_dir => "data/"
)

# Default feeds
const FEEDS = [
    Dict("name" => "BBC", "url" => "http://feeds.bbci.co.uk/news/world/rss.xml", "category" => "World"),
    Dict("name" => "TechCrunch", "url" => "https://techcrunch.com/feed/", "category" => "Tech"),
]

# Fetch RSS feed
function fetch_feed(url::String)
    try
        response = HTTP.get(url, ["User-Agent" => CONFIG[:user_agent]])
        return String(response.body)
    catch e
        println("Error fetching $url: $e")
        return ""
    end
end

# Parse RSS items (simplified)
function parse_rss(xml::String, source::String)
    items = []
    
    # Simple regex-based extraction
    title_pattern = r"<title>([^<]+)</title>"
    link_pattern = r"<link>([^<]+)</link>"
    desc_pattern = r"<description>([^<]+)</description>"
    
    titles = matchall(title_pattern, xml)
    links = matchall(link_pattern, xml)
    descs = matchall(desc_pattern, xml)
    
    for i in 1:min(length(titles), 20)
        item = Dict(
            "title" => titles[i].captures[1],
            "source" => source,
            "category" => "General",
            "sentiment" => "neutral",
            "reading_time" => 1
        )
        push!(items, item)
    end
    
    return items
end

# Analyze sentiment
function analyze_sentiment(text::String)
    text = lowercase(text)
    
    positive = ["good", "great", "excellent", "amazing", "breakthrough", "success", "win"]
    negative = ["bad", "terrible", "crisis", "fail", "death", "war", "attack", "disaster"]
    
    pos_count = sum(contains(text, w) for w in positive)
    neg_count = sum(contains(text, w) for w in negative)
    
    if pos_count > neg_count
        return "positive"
    elseif neg_count > pos_count
        return "negative"
    else
        return "neutral"
    end
end

# Extract keywords
function extract_keywords(text::String, n::Int=10)
    stop_words = Set(["the", "a", "an", "and", "or", "but", "in", "on", "at", "to", 
                     "for", "of", "with", "by", "from", "is", "are", "was", "were"])
    
    words = split(lowercase(text), r"\W+")
    words = [w for w in words if length(w) > 3 && !(w in stop_words)]
    
    freq = Dict{String, Int}()
    for w in words
        freq[w] = get(freq, w, 0) + 1
    end
    
    sorted = sort(collect(freq), by=x->x[2], rev=true)
    return [k for (k, v) in sorted[1:min(n, length(sorted))]]
end

# Calculate statistics
function calculate_stats(items::Vector{Dict{String, Any}})
    if isempty(items)
        return Dict()
    end
    
    sentiments = [item["sentiment"] for item in items]
    pos = sum(s -> s == "positive", sentiments)
    neg = sum(s -> s == "negative", sentiments)
    neu = sum(s -> s == "neutral", sentiments)
    
    return Dict(
        "total" => length(items),
        "positive" => pos,
        "negative" => neg,
        "neutral" => neu,
        "avg_reading_time" => mean([item["reading_time"] for item in items])
    )
end

# Main function
function main(args::Vector{String})
    println("Tanya RSS Analyzer (Julia)")
    println("===========================")
    println()
    
    if "--help" in args || "-h" in args
        println("Usage: julia analyzer.jl [options]")
        println()
        println("Options:")
        println("  --url URL    Analyze specific URL")
        println("  --all       Analyze all feeds (default)")
        println("  --stats     Show statistics")
        return
    end
    
    # Determine feeds to analyze
    feeds_to_analyze = FEEDS
    if "--url" in args
        idx = findfirst(args .== "--url")
        if idx !== nothing && length(args) > idx
            feeds_to_analyze = [Dict("name" => "Custom", "url" => args[idx+1], "category" => "General")]
        end
    end
    
    all_items = []
    for feed in feeds_to_analyze
        println("Fetching $(feed["name"])...")
        xml = fetch_feed(feed["url"])
        
        if !isempty(xml)
            items = parse_rss(xml, feed["name"])
            
            # Analyze each item
            for item in items
                item["sentiment"] = analyze_sentiment(item["title"])
                item["keywords"] = extract_keywords(item["title"])
            end
            
            append!(all_items, items)
            println("  -> Found $(length(items)) articles")
        end
    end
    
    println()
    println("Total articles: $(length(all_items))")
    
    # Statistics
    if "--stats" in args
        stats = calculate_stats(all_items)
        println()
        println("=== Statistics ===")
        for (k, v) in stats
            println("$k: $v")
        end
    end
    
    println()
    println("Engine: Julia (scientific computing)")
end

# Run
main(ARGS)
