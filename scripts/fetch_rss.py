import feedparser
import json
import os
from datetime import datetime, timezone
import urllib.request

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

SOURCES = config["sources"]
TOPICS = config["topics"]

def tag_article(title, description=""):
    text = (title + " " + description).lower()
    matched = []
    for topic, keywords in TOPICS.items():
        for kw in keywords:
            if kw.lower() in text:
                matched.append(topic)
                break
    return matched if matched else ["기타"]

def parse_date(entry):
    for attr in ["published_parsed", "updated_parsed"]:
        val = getattr(entry, attr, None)
        if val:
            try:
                dt = datetime(*val[:6], tzinfo=timezone.utc)
                return dt.isoformat()
            except Exception:
                pass
    return datetime.now(timezone.utc).isoformat()

def fetch_feed(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; RSS Reader)"
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read()
        return feedparser.parse(content)
    except Exception as e:
        print(f"  Request error: {e}")
        return feedparser.parse(url)

def fetch_all():
    articles = []
    seen_urls = set()

    for source in SOURCES:
        print(f"Fetching {source['name']}...")
        try:
            feed = fetch_feed(source["rss"])
            count = 0
            for entry in feed.entries[:30]:
                url = entry.get("link", "")
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)
                title = entry.get("title", "").strip()
                if not title:
                    continue
                description = entry.get("summary", "")
                topics = tag_article(title, description)
                date = parse_date(entry)
                articles.append({
                    "id": str(abs(hash(url))),
                    "title": title,
                    "url": url,
                    "source": source["name"],
                    "topics": topics,
                    "date": date
                })
                count += 1
            print(f"  -> {count} articles")
        except Exception as e:
            print(f"  Error: {e}")

    articles.sort(key=lambda x: x["date"], reverse=True)

    output = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "total": len(articles),
        "articles": articles
    }

    os.makedirs("public", exist_ok=True)
    with open("public/articles.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nDone! {len(articles)} articles saved to public/articles.json")

if __name__ == "__main__":
    fetch_all()
