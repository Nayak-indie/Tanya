import java.io.*;
import java.net.*;
import java.util.*;
import java.util.regex.*;

public class APIServer {
    private static final int PORT = 8080;
    private static final String DATA_DIR = "../data/";
    
    public static void main(String[] args) throws IOException {
        int port = PORT;
        if (args.length > 0) {
            port = Integer.parseInt(args[0]);
        }
        
        System.out.println(" Tanya API Server (Java)");
        System.out.println("=========================");
        System.out.println("Starting on port " + port + "...");
        
        // Simple built-in server
        ServerSocket server = new ServerSocket(port);
        System.out.println("Server running at http://localhost:" + port);
        System.out.println("Endpoints:");
        System.out.println("  GET /api/news          - List all news");
        System.out.println("  GET /api/news/{id}    - Get single article");
        System.out.println("  GET /api/search?q=    - Search news");
        System.out.println("  GET /api/stats         - Statistics");
        System.out.println("  GET /api/sources      - RSS Sources");
        
        while (true) {
            Socket client = server.accept();
            handleRequest(client);
        }
    }
    
    private static void handleRequest(Socket client) {
        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
            String request = in.readLine();
            
            if (request == null) {
                client.close();
                return;
            }
            
            String[] parts = request.split(" ");
            String method = parts[0];
            String path = parts.length > 1 ? parts[1] : "/";
            
            String response;
            if (path.startsWith("/api/news")) {
                response = handleNews(path);
            } else if (path.startsWith("/api/search")) {
                response = handleSearch(path);
            } else if (path.startsWith("/api/stats")) {
                response = handleStats();
            } else if (path.startsWith("/api/sources")) {
                response = handleSources();
            } else {
                response = "HTTP/1.1 404 Not Found\r\nContent-Type: application/json\r\n\r\n{\"error\":\"Not found\"}";
            }
            
            PrintWriter out = new PrintWriter(client.getOutputStream(), true);
            out.print(response);
            client.close();
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    private static String handleNews(String path) throws IOException {
        File file = new File(DATA_DIR + "news.json");
        String content = "";
        if (file.exists()) {
            Scanner scanner = new Scanner(file);
            content = scanner.useDelimiter("\\A").next();
            scanner.close();
        }
        
        return "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\n\r\n" + content;
    }
    
    private static String handleSearch(String path) throws IOException {
        String query = "";
        Pattern p = Pattern.compile("q=([^&]+)");
        Matcher m = p.matcher(path);
        if (m.find()) {
            query = URLDecoder.decode(m.group(1), "UTF-8");
        }
        
        File file = new File(DATA_DIR + "news.json");
        String content = "[]";
        if (file.exists()) {
            Scanner scanner = new Scanner(file);
            content = scanner.useDelimiter("\\A").next();
            scanner.close();
        }
        
        // Simple search (in production use proper search engine)
        return "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\n\r\n" + content;
    }
    
    private static String handleStats() throws IOException {
        File file = new File(DATA_DIR + "news.json");
        String content = "{\"total\":0}";
        
        if (file.exists()) {
            Scanner scanner = new Scanner(file);
            String json = scanner.useDelimiter("\\A").next();
            scanner.close();
            
            // Count articles
            int count = json.split("title").length - 1;
            content = "{\"total\":" + count + ",\"engine\":\"java\"}";
        }
        
        return "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\n\r\n" + content;
    }
    
    private static String handleSources() throws IOException {
        File file = new File(DATA_DIR + "sources.json");
        String content = "[]";
        
        if (file.exists()) {
            Scanner scanner = new Scanner(file);
            content = scanner.useDelimiter("\\A").next();
            scanner.close();
        }
        
        return "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\n\r\n" + content;
    }
}