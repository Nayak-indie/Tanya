-- Tanya RSS Scraper in Lua
-- Run: lua lua/scraper.lua [--url URL] [--help]
-- Requires: lua, luasocket

local socket = require("socket")

-- Configuration
local CONFIG = {
    timeout = 10,
    user_agent = "Tanya/1.0 RSS Reader (Lua)",
    data_dir = "data/",
}

-- RSS Feed sources
local SOURCES = {
    {name = "BBC", url = "http://feeds.bbci.co.uk/news/world/rss.xml", category = "World"},
    {name = "TechCrunch", url = "https://techcrunch.com/feed/", category = "Tech"},
    {name = "HackerNews", url = "https://hnrss.org/frontpage", category = "Tech"},
}

-- Fetch URL
local function fetch(url)
    local client = socket.try(socket.connect("80", 3))
    client:settimeout(CONFIG.timeout)
    
    local request = string.format(
        "GET %s HTTP/1.0\r\nHost: %s\r\nUser-Agent: %s\r\n\r\n",
        url, url:match("([^/]+)"), CONFIG.user_agent
    )
    
    client:send(request)
    
    local response = {}
    while true do
        local chunk, err = client:receive("*a")
        if err then break end
        table.insert(response, chunk)
    end
    
    client:close()
    return table.concat(response)
end

-- Parse RSS
local function parse_rss(xml, source_name)
    local items = {}
    
    -- Simple pattern matching
    for title in xml:gmatch("<title><!%[CDATA%[(.-)%]%]></title>") do
        table.insert(items, {title = title, source = source_name})
    end
    for title in xml:gmatch("<title>(.-)</title>") do
        if title ~= "" and title ~= source_name then
            table.insert(items, {title = title, source = source_name})
        end
    end
    
    return items
end

-- Estimate reading time
local function reading_time(text)
    local words = {}
    for word in text:gmatch("%S+") do
        table.insert(words, word)
    end
    return math.max(1, math.ceil(#words / 200))
end

-- Sentiment analysis
local function sentiment(title, desc)
    local text = (title .. " " .. desc):lower()
    
    local positive = {good = true, great = true, excellent = true, amazing = true, 
                      breakthrough = true, success = true, win = true}
    local negative = {bad = true, terrible = true, crisis = true, fail = true,
                      death = true, war = true, attack = true, disaster = true}
    
    local pos, neg = 0, 0
    for word in text:gmatch("%a+") do
        if positive[word] then pos = pos + 1 end
        if negative[word] then neg = neg + 1 end
    end
    
    if pos > neg then return "positive"
    elseif neg > pos then return "negative"
    else return "neutral"
    end
end

-- Extract keywords
local function keywords(title, desc)
    local stop_words = {
        the = true, a = true, an = true, and = true, or = true, but = true,
        in = true, on = true, at = true, to = true, for = true, of = true,
        with = true, by = true, from = true, is = true, are = true
    }
    
    local freq = {}
    local text = (title .. " " .. desc):lower()
    for word in text:gmatch("%a+") do
        if #word > 3 and not stop_words[word] then
            freq[word] = (freq[word] or 0) + 1
        end
    end
    
    local sorted = {}
    for word, count in pairs(freq) do
        table.insert(sorted, {word = word, count = count})
    end
    table.sort(sorted, function(a, b) return a.count > b.count end)
    
    local result = {}
    for i, item in ipairs(sorted) do
        if i > 10 then break end
        table.insert(result, item.word)
    end
    return result
end

-- Main
local function main(args)
    print("Tanya RSS Scraper (Lua)")
    print("========================")
    print("")
    
    if #args > 0 and args[1] == "--help" then
        print("Usage: lua scraper.lua [options]")
        print("")
        print("Options:")
        print("  --url URL    Fetch specific URL")
        print("  --all       Fetch all sources (default)")
        print("  --help      Show this help")
        return
    end
    
    -- Default: fetch all
    local to_fetch = SOURCES
    if #args > 0 and args[1] == "--url" then
        to_fetch = {{name = "Custom", url = args[2], category = "General"}}
    end
    
    local total = 0
    for _, source in ipairs(to_fetch) do
        print(string.format("Fetching %s...", source.name))
        
        local response = fetch(source.url)
        local items = parse_rss(response, source.name)
        
        print(string.format("  -> Found %d articles", #items))
        total = total + #items
    end
    
    print("")
    print(string.format("Total: %d articles fetched", total))
    print("Engine: Lua (lightweight & fast)")
end

main(arg)
