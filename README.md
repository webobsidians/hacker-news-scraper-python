# Scrape Hacker News with Python (Search, Front Page and Who Is Hiring Jobs)

Search Hacker News stories and comments, read the front page and collect every job post of the monthly "Who is hiring?" thread with two free public APIs, or use a ready-made Apify Actor that also monitors new items.

> This example was written with the help of AI. The code was run and checked on 20 November 2026 before publishing.

Hacker News is unusually friendly to code: it has an official read-only API and a free full-text search API, and neither needs a key. The hard parts are knowing which one to use for what, turning the HTML text into something readable, and getting at the job posts hidden in the monthly "Who is hiring?" thread. This post shows a short Python script for all three, and a no-code option for when you need monitoring or a clean export.

## How it works
- **Algolia search** (`hn.algolia.com/api/v1/`) finds stories and comments by keyword, author or date, newest first with `search_by_date`.
- **The official Firebase API** (`hacker-news.firebaseio.com/v0/`) gives the lists (`topstories`, `newstories`, `beststories`, `askstories`, `showstories`, `jobstories`) and any item by ID.
- **"Who is hiring?"** is a story posted by the user `whoishiring` every month. Each job post is a top-level comment, and Algolia's `items/<id>` returns the whole thread in one request.

The script is in [`hacker_news_scraper.py`](hacker_news_scraper.py).

A few things worth knowing before you build on it:

- **Tags** combine with commas (AND) and parentheses (OR): `(story,comment)` finds both, `comment,author_pg` finds the comments of one user, and `ask_hn` or `show_hn` narrow stories further.
- **Dates and points** go in `numericFilters`, for example `created_at_i>1767225600,points>50`.
- **`search` vs `search_by_date`:** the first sorts by relevance, the second newest first. Use the second for monitoring.
- **1,000 hits per query** is the hard limit of the search API. For more, split the query into date ranges.
- **Text is HTML** with `<p>`, `<i>`, `<a>` and escaped characters. Convert it before you analyse it, and keep the link addresses, which HN puts in `href`.
- **Lists hold up to 500 IDs.** Each item is one more request, so fetch them in parallel, politely.
- **Job posts are free text.** Most start with a line such as `Company | Role | Location | Remote | Salary`, but it is the poster's own words, so split on `|` and treat the parts as hints.

For a quick look, this script is all you need.

## Run it

```bash
python hacker_news_scraper.py
```

## Hosted version

For many sources, a schedule, "only new items" monitoring or CSV/Excel exports, the same approach runs as the [Hacker News Scraper](https://apify.com/webobsidians/hacker-news-scraper) on Apify. Disclosure: it is built and sold by Web Obsidians, who publish this repository.

## License

MIT
