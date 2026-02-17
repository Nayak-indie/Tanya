using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;

namespace Tanya.Notifications
{
    /// <summary>
    /// Tanya Notification Service (C#)
    /// Handles browser notifications and email alerts
    /// </summary>
    public class NotificationService
    {
        private readonly HttpClient _httpClient;
        private readonly string _pushoverAppToken;
        private readonly string _pushoverUserKey;
        
        public NotificationService()
        {
            _httpClient = new HttpClient();
        }

        /// <summary>
        /// Send browser notification
        /// </summary>
        public async Task SendBrowserNotification(string title, string message, string icon = "📰")
        {
            var notification = new
            {
                title,
                body = message,
                icon,
                timestamp = DateTimeOffset.UtcNow.ToUnixTimeSeconds()
            };
            
            Console.WriteLine($"[Browser Notification] {title}: {message}");
            await Task.CompletedTask;
        }

        /// <summary>
        /// Send email notification
        /// </summary>
        public async Task SendEmailNotification(string to, string subject, string body)
        {
            // In production, use SendGrid, Mailgun, or SMTP
            var email = new
            {
                to,
                subject,
                body,
                from = "tanya@notifications.local"
            };
            
            Console.WriteLine($"[Email] To: {to}, Subject: {subject}");
            await Task.CompletedTask;
        }

        /// <summary>
        /// Send push notification via Pushover
        /// </summary>
        public async Task SendPushoverNotification(string title, string message, int priority = 0)
        {
            var form = new Dictionary<string, string>
            {
                ["token"] = _pushoverAppToken ?? "",
                ["user"] = _pushoverUserKey ?? "",
                ["title"] = title,
                ["message"] = message,
                ["priority"] = priority.ToString()
            };

            try
            {
                var response = await _httpClient.PostAsync(
                    "https://api.pushover.net/1/messages.json",
                    new FormContent(form));
                
                Console.WriteLine($"[Pushover] Notification sent: {title}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Pushover error: {ex.Message}");
            }
        }
    }

    /// <summary>
    /// Keyword alert monitor
    /// </summary>
    public class KeywordAlerter
    {
        private readonly List<string> _keywords;
        private readonly NotificationService _notifications;
        private readonly string _alertChannel;

        public KeywordAlerter(List<string> keywords, string alertChannel = "browser")
        {
            _keywords = keywords;
            _notifications = new NotificationService();
            _alertChannel = alertChannel;
        }

        public async Task CheckArticle(Article article)
        {
            var content = $"{article.Title} {article.Content}".ToLower();

            foreach (var keyword in _keywords)
            {
                if (content.Contains(keyword.ToLower()))
                {
                    var message = $"Found keyword '{keyword}' in: {article.Title}";

                    switch (_alertChannel.ToLower())
                    {
                        case "email":
                            await _notifications.SendEmailNotification(
                                "user@example.com",
                                $"Keyword Alert: {keyword}",
                                message);
                            break;
                        case "pushover":
                            await _notifications.SendPushoverNotification(
                                $"Keyword: {keyword}",
                                article.Title);
                            break;
                        default:
                            await _notifications.SendBrowserNotification(
                                $"Keyword: {keyword}",
                                article.Title);
                            break;
                    }
                }
            }
        }
    }

    public class Article
    {
        public string Id { get; set; }
        public string Title { get; set; }
        public string Content { get; set; }
        public string Link { get; set; }
        public DateTime Published { get; set; }
    }

    public class Program
    {
        public static async Task Main(string[] args)
        {
            var notifier = new NotificationService();
            
            await notifier.SendBrowserNotification(
                "New Articles Available",
                "5 new articles collected from your feeds");

            var alerter = new KeywordAlerter(
                new List<string> { "AI", "breakthrough", "news" });
            
            await alerter.CheckArticle(new Article
            {
                Id = "1",
                Title = "AI Breakthrough Announced",
                Content = "Scientists reveal new AI technology"
            });
        }
    }
}
