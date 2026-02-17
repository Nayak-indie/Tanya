package com.tanya.api;

import com.sun.net.httpserver.*;
import java.io.*;
import java.net.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.Collectors;

/**
 * Tanya REST API Server (Java)
 * Exposes endpoints for article management, search, and export
 */
public class ApiServer {
    private final HttpServer server;
    private final Map<String, Map<String, Object>> articles = new ConcurrentHashMap<>();
    private final SearchEngine searchEngine = new SearchEngine();
    private static final int PORT = 8080;

    public ApiServer() throws IOException {
        this.server = HttpServer.create(new InetSocketAddress(PORT), 0);
        setupRoutes();
    }

    private void setupRoutes() {
        server.createContext("/api/articles", this::handleArticles);
        server.createContext("/api/search", this::handleSearch);
        server.createContext("/api/export/json", this::handleExportJson);
        server.createContext("/api/export/csv", this::handleExportCsv);
        server.createContext("/api/favorites", this::handleFavorites);
        server.createContext("/api/analyze", this::handleAnalyze);
        server.setExecutor(Executors.newFixedThreadPool(10));
    }

    private void handleArticles(HttpExchange exchange) throws IOException {
        String method = exchange.getRequestMethod();
        String path = exchange.getRequestURI().getPath();
        
        if ("GET".equals(method)) {
            sendJson(exchange, articles.values().stream()
                .map(a -> (Object)a)
                .collect(Collectors.toList()));
        } else if ("POST".equals(method)) {
            String body = readBody(exchange);
            Map<String, Object> article = parseJson(body);
            String id = UUID.randomUUID().toString();
            article.put("id", id);
            article.put("saved_at", System.currentTimeMillis());
            articles.put(id, article);
            searchEngine.index(article);
            sendJson(exchange, article);
        }
    }

    private void handleSearch(HttpExchange exchange) throws IOException {
        String query = parseQueryParams(exchange.getRequestURI()).getOrDefault("q", "");
        List<Map<String, Object>> results = searchEngine.search(query, 20);
        sendJson(exchange, results);
    }

    private void handleExportJson(HttpExchange exchange) throws IOException {
        String json = toJson(articles.values());
        exchange.getResponseHeaders().set("Content-Type", "application/json");
        exchange.getResponseHeaders().set("Content-Disposition", "attachment; filename=articles.json");
        exchange.sendResponseHeaders(200, json.getBytes().length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(json.getBytes());
        }
    }

    private void handleExportCsv(HttpExchange exchange) throws IOException {
        StringBuilder csv = new StringBuilder("id,title,link,published,sentiment,reading_time\n");
        for (Map<String, Object> a : articles.values()) {
            csv.append(escapeCsv(a.get("id")))
               .append(",").append(escapeCsv(a.get("title")))
               .append(",").append(escapeCsv(a.get("link")))
               .append(",").append(escapeCsv(a.get("published")))
               .append(",").append(escapeCsv(a.get("sentiment")))
               .append(",").append(escapeCsv(a.get("reading_time")))
               .append("\n");
        }
        byte[] bytes = csv.toString().getBytes();
        exchange.getResponseHeaders().set("Content-Type", "text/csv");
        exchange.getResponseHeaders().set("Content-Disposition", "attachment; filename=articles.csv");
        exchange.sendResponseHeaders(200, bytes.length);
        try (OutputStream os = exchange.getResponseBody()) { os.write(bytes); }
    }

    private void handleFavorites(HttpExchange exchange) throws IOException {
        List<Map<String, Object>> favs = articles.values().stream()
            .filter(a -> Boolean.TRUE.equals(a.get("is_favorite")))
            .collect(Collectors.toList());
        sendJson(exchange, favs);
    }

    private void handleAnalyze(HttpExchange exchange) throws IOException {
        String body = readBody(exchange);
        Map<String, Object> data = parseJson(body);
        String text = (String) data.getOrDefault("text", "");
        
        Map<String, Object> analysis = new HashMap<>();
        analysis.put("sentiment", SentimentAnalyzer.analyze(text));
        analysis.put("reading_time", ReadingTimeCalculator.calculate(text));
        analysis.put("keywords", KeywordExtractor.extract(text));
        analysis.put("sentiment_score", SentimentAnalyzer.getScore(text));
        
        sendJson(exchange, analysis);
    }

    public void start() {
        server.start();
        System.out.println("Tanya API Server running on port " + PORT);
    }

    private void sendJson(HttpExchange exchange, Object data) throws IOException {
        String json = toJson(Collections.singletonList(data));
        if (data instanceof Collection) json = toJson((Collection<?>) data);
        else json = toJson(Collections.singletonList(data));
        
        exchange.getResponseHeaders().set("Content-Type", "application/json");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        byte[] bytes = json.getBytes();
        exchange.sendResponseHeaders(200, bytes.length);
        try (OutputStream os = exchange.getResponseBody()) { os.write(bytes); }
    }

    private String readBody(HttpExchange ex) throws IOException {
        try (BufferedReader br = new BufferedReader(new InputStreamReader(ex.getRequestBody()))) {
            return br.lines().collect(Collectors.joining());
        }
    }

    private Map<String, Object> parseJson(String json) {
        Map<String, Object> m = new HashMap<>();
        // Simplified - use Jackson/Gson in production
        return m;
    }

    private Map<String, String> parseQueryParams(URI uri) {
        Map<String, String> params = new HashMap<>();
        if (uri.getQuery() != null) {
            for (String p : uri.getQuery().split("&")) {
                String[] kv = p.split("=");
                if (kv.length == 2) params.put(kv[0], kv[1]);
            }
        }
        return params;
    }

    private String toJson(Collection<?> c) {
        StringBuilder sb = new StringBuilder("[");
        Iterator<?> it = c.iterator();
        while (it.hasNext()) {
            sb.append(it.next().toString());
            if (it.hasNext()) sb.append(",");
        }
        sb.append("]");
        return sb.toString();
    }

    private String escapeCsv(Object o) {
        if (o == null) return "";
        String s = o.toString();
        if (s.contains(",") || s.contains("\"") || s.contains("\n")) {
            return "\"" + s.replace("\"", "\"\"") + "\"";
        }
        return s;
    }

    public static void main(String[] args) throws IOException {
        new ApiServer().start();
    }
}

// Supporting classes
class SearchEngine {
    private final Map<String, Map<String, Object>> index = new ConcurrentHashMap<>();
    
    public void index(Map<String, Object> article) {
        String id = (String) article.get("id");
        index.put(id, article);
    }
    
    public List<Map<String, Object>> search(String query, int limit) {
        String[] terms = query.toLowerCase().split("\\s+");
        return index.values().stream()
            .filter(a -> {
                String text = ((String)a.getOrDefault("title", "")).toLowerCase() + 
                              ((String)a.getOrDefault("content", "")).toLowerCase();
                return Arrays.stream(terms).allMatch(text::contains);
            })
            .limit(limit)
            .collect(Collectors.toList());
    }
}

class SentimentAnalyzer {
    private static final Map<String, Integer> POSITIVE = Map.of(
        "good", 1, "great", 2, "excellent", 3, "amazing", 3, "success", 2, "breakthrough", 2
    );
    private static final Map<String, Integer> NEGATIVE = Map.of(
        "bad", -1, "terrible", -3, "horrible", -3, "failure", -2, "crisis", -2, "disaster", -2
    );
    
    public static String analyze(String text) {
        int score = getScore(text);
        if (score > 0) return "positive";
        if (score < 0) return "negative";
        return "neutral";
    }
    
    public static int getScore(String text) {
        int score = 0;
        for (String word : text.toLowerCase().split("\\W+")) {
            score += POSITIVE.getOrDefault(word, 0);
            score += NEGATIVE.getOrDefault(word, 0);
        }
        return score;
    }
}

class ReadingTimeCalculator {
    private static final int WPM = 200;
    
    public static int calculate(String text) {
        int words = text.split("\\s+").length;
        return Math.max(1, (int) Math.ceil((double) words / WPM));
    }
}

class KeywordExtractor {
    public static List<String> extract(String text) {
        Set<String> keywords = new HashSet<>();
        String[] words = text.toLowerCase().split("\\W+");
        for (String w : words) {
            if (w.length() > 5) keywords.add(w);
        }
        return new ArrayList<>(keywords);
    }
}
