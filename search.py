"""Real search results, fetched server-side from Wikipedia's public API."""
import json
import urllib.parse
import urllib.request

API_URL = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "PrivSearch/1.0 (student portfolio project)"


def search_web(query, limit=5):
    """Return a list of result dicts: {title, url, engine}."""
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": limit,
        }
    )
    request = urllib.request.Request(
        API_URL + "?" + params,
        headers={"User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(request, timeout=5) as response:
        data = json.load(response)

    results = []
    for item in data.get("query", {}).get("search", []):
        title = item["title"]
        results.append(
            {
                "title": title,
                "url": "https://en.wikipedia.org/wiki/"
                + urllib.parse.quote(title.replace(" ", "_")),
                "engine": "wikipedia",
            }
        )
    return results


if __name__ == "__main__":
    for r in search_web("python"):
        print(f"- {r['title']}  ->  {r['url']}")
