import feedparser
import json
import smtplib
from email.mime.text import MIMEText
from pathlib import Path

RSS_FEEDS = [
    "https://hartford.craigslist.org/search/apa?format=rss&query=farmington&max_price=3000&min_bedrooms=2&max_bedrooms=3",
]

DATA_FILE = "seen.json"

EMAIL_FROM = "YOUR_EMAIL@gmail.com"
EMAIL_TO = "YOUR_EMAIL@gmail.com"
EMAIL_PASS = "APP_PASSWORD"


def load_seen():
    if Path(DATA_FILE).exists():
        return set(json.load(open(DATA_FILE)))
    return set()


def save_seen(seen):
    json.dump(list(seen), open(DATA_FILE, "w"))


def fetch_listings():
    listings = []
    for feed in RSS_FEEDS:
        f = feedparser.parse(feed)
        for entry in f.entries:
            listings.append({
                "title": entry.title,
                "link": entry.link
            })
    return listings


def send_email(new_items):

    body = "\n\n".join(
        f"{i['title']}\n{i['link']}" for i in new_items
    )

    msg = MIMEText(body)
    msg["Subject"] = "New Farmington Rentals"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASS)
        server.send_message(msg)


def main():

    seen = load_seen()
    listings = fetch_listings()

    new_items = [i for i in listings if i["link"] not in seen]

    if new_items:
        send_email(new_items)

    for i in listings:
        seen.add(i["link"])

    save_seen(seen)


if __name__ == "__main__":
    main()
