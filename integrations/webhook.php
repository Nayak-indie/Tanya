<?php
/**
 * Tanya - Webhook Handler (PHP)
 * Handles incoming webhooks and outgoing notifications
 */

// Configuration
define('API_SECRET', getenv('TANYA_API_SECRET') ?: 'secret123');
define('LOG_FILE', '/tmp/tanya-webhook.log');

/**
 * Log messages to file
 */
function log_msg($msg) {
    $timestamp = date('Y-m-d H:i:s');
    file_put_contents(LOG_FILE, "[$timestamp] $msg\n", FILE_APPEND);
}

/**
 * Verify webhook signature
 */
function verify_signature($payload, $signature) {
    $expected = hash_hmac('sha256', $payload, API_SECRET);
    return hash_equals($expected, $signature);
}

/**
 * Send notification to Slack
 */
function send_slack($channel, $message, $username = 'Tanya') {
    $webhook = getenv('SLACK_WEBHOOK_URL');
    if (!$webhook) return false;
    
    $data = [
        'channel' => $channel,
        'username' => $username,
        'text' => $message,
        'icon_emoji' => ':newspaper:'
    ];
    
    $ch = curl_init($webhook);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $result = curl_exec($ch);
    curl_close($ch);
    
    return $result;
}

/**
 * Send notification to Discord
 */
function send_discord($webhook_url, $message, $title = 'Tanya News') {
    $embed = [
        'title' => $title,
        'description' => $message,
        'color' => 5814784,
        'timestamp' => date('c')
    ];
    
    $data = ['embeds' => [$embed]];
    
    $ch = curl_init($webhook_url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $result = curl_exec($ch);
    curl_close($ch);
    
    return $result;
}

/**
 * Parse incoming webhook
 */
function parse_webhook($input) {
    $data = json_decode($input, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        return ['error' => 'Invalid JSON'];
    }
    
    return [
        'action' => $data['action'] ?? 'unknown',
        'article' => $data['article'] ?? null,
        'timestamp' => time()
    ];
}

/**
 * Process RSS update webhook
 */
function handle_rss_update($data) {
    $article = $data['article'];
    $message = "New article: {$article['title']}";
    
    log_msg("RSS Update: " . $article['title']);
    
    // Send to configured channels
    if ($slack = getenv('SLACK_WEBHOOK_URL')) {
        send_slack('#news', $message);
    }
    
    return ['status' => 'processed', 'message' => $message];
}

/**
 * Process keyword alert webhook
 */
function handle_keyword_alert($data) {
    $keyword = $data['keyword'] ?? 'unknown';
    $article = $data['article'];
    
    $message = "🔔 Keyword alert '$keyword': {$article['title']}";
    log_msg("Keyword Alert: $keyword - {$article['title']}");
    
    return ['status' => 'alert_sent', 'keyword' => $keyword];
}

// Main webhook handler
header('Content-Type: application/json');

$method = $_SERVER['REQUEST_METHOD'];
$input = file_get_contents('php://input');

if ($method === 'POST') {
    // Verify signature if provided
    $signature = $_SERVER['HTTP_X_SIGNATURE'] ?? '';
    if ($signature && !verify_signature($input, $signature)) {
        http_response_code(401);
        echo json_encode(['error' => 'Invalid signature']);
        exit;
    }
    
    $data = parse_webhook($input);
    
    if (isset($data['error'])) {
        http_response_code(400);
        echo json_encode($data);
        exit;
    }
    
    // Route to handler
    $result = match($data['action']) {
        'rss_update' => handle_rss_update($data),
        'keyword_alert' => handle_keyword_alert($data),
        default => ['status' => 'unknown_action']
    };
    
    echo json_encode($result);
} elseif ($method === 'GET') {
    // Health check
    echo json_encode(['status' => 'ok', 'timestamp' => time()]);
} else {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
}

// CLI test
if (php_sapi_name() === 'cli' && $argc > 1) {
    $test = ['action' => 'rss_update', 'article' => ['title' => 'Test Article']];
    print_r(handle_rss_update($test));
}
?>
