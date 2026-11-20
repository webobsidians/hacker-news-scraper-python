import html
import json
import re
import urllib.parse
import urllib.request

ALGOLIA = "https://hn.algolia.com/api/v1/"


def get(url):
    with urllib.request.urlopen(url) as r:
        return json.load(r)


def text(s):
    s = re.sub(r"<p>", "\n\n", s or "")
    s = re.sub(r'<a\s[^>]*href="([^"]*)"[^>]*>.*?</a>', lambda m: m.group(1), s)
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def mentions(term, limit=50):
    q = urllib.parse.urlencode({"query": term, "tags": "(story,comment)", "hitsPerPage": limit})
    return get(ALGOLIA + "search_by_date?" + q)["hits"]


def who_is_hiring():
    q = urllib.parse.urlencode({"query": "who is hiring", "tags": "story,author_whoishiring", "hitsPerPage": 10})
    thread = next(h for h in get(ALGOLIA + "search_by_date?" + q)["hits"]
                  if h["title"].startswith("Ask HN: Who is hiring?"))
    tree = get(ALGOLIA + f"items/{thread['objectID']}")
    return tree["title"], [text(c["text"]) for c in tree["children"] if c.get("text")]


for h in mentions("llm", 5):
    kind = "comment" if "comment" in h["_tags"] else "story"
    print(h["created_at"][:16], kind, h["author"], (h.get("title") or text(h.get("comment_text")))[:60])

title, posts = who_is_hiring()
print(title, len(posts), "job posts")
for p in posts[:5]:
    print(" ", p.split("\n")[0][:100])
