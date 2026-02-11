import feedparser
from datetime import datetime

class NewsService:
    """뉴스 RSS 피드 서비스"""
    
    def __init__(self):
        self.feeds = {
            "cnbc": {
                "url": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
                "name": "CNBC"
            },
            "bloomberg": {
                "url": "https://www.bloomberg.com/feed/podcast/etf-report.xml",
                "name": "Bloomberg"
            },
            "wsj": {
                "url": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
                "name": "Wall Street Journal"
            }
        }
    
    def get_all_news(self, limit=5):
        """모든 뉴스 소스에서 헤드라인 가져오기"""
        try:
            result = {}
            
            for source_key, source_info in self.feeds.items():
                articles = self._fetch_feed(source_info["url"], source_info["name"], limit)
                result[source_key] = {
                    "source": source_info["name"],
                    "articles": articles
                }
            
            return {
                "success": True,
                "data": result,
                "updated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error fetching news: {e}")
            return {
                "success": False,
                "error": str(e),
                "data": None
            }
    
    def get_news_by_source(self, source, limit=5):
        """특정 소스의 뉴스만 가져오기"""
        try:
            if source not in self.feeds:
                return {
                    "success": False,
                    "error": f"Unknown source: {source}"
                }
            
            source_info = self.feeds[source]
            articles = self._fetch_feed(source_info["url"], source_info["name"], limit)
            
            return {
                "success": True,
                "data": {
                    "source": source_info["name"],
                    "articles": articles
                },
                "updated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error fetching {source} news: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _fetch_feed(self, url, source_name, limit):
        """RSS 피드 파싱"""
        try:
            feed = feedparser.parse(url)
            articles = []
            
            for entry in feed.entries[:limit]:
                article = {
                    "title": entry.get("title", "No title"),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "summary": entry.get("summary", "")[:200] + "..." if len(entry.get("summary", "")) > 200 else entry.get("summary", "")
                }
                articles.append(article)
            
            return articles
            
        except Exception as e:
            print(f"Error parsing {source_name} feed: {e}")
            return []
