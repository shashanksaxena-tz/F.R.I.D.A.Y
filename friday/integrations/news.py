import feedparser
from .base import Integration

class NewsIntegration(Integration):
    def get_name(self):
        return "News Feed"

    def execute(self, limit=3):
        try:
            # Using Google News RSS (US Edition)
            feed = feedparser.parse("https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en")
            headlines = [entry.title for entry in feed.entries[:limit]]
            return ". ".join(headlines)
        except Exception as e:
            return f"Error fetching news: {str(e)}"
