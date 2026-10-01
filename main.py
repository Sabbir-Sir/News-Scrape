import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

url = "https://www.bbc.com/news"
header = {"User-Agent": "Mozilla/5.0"}
all_news = []

for page in range(1, 4):

    page_url = f"{url}?page={page}"

    response = requests.get(page_url, headers=header, timeout=10)
    # Added a timeout so the program does not wait forever for a response.

    if response.status_code != 200:
        print(f"Page {page} could not be accessed.")
        continue
    # Checks if the page was successfully loaded before scraping it.

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("a", href=True)

    for j in articles:

        title_tag = j.find(["h2", "h3"])

        if title_tag:
            title = title_tag.get_text(strip=True)
        else:
            title = "N/A"

        summary_tag = j.find("p")

        if summary_tag:
            summary = summary_tag.get_text(strip=True)
        else:
            summary = "N/A"

        link = j.get("href")

        if link:
            article_url = urljoin(url, link)
        else:
            article_url = "N/A"

        author = "N/A"

        if article_url != "N/A":
            article_response = requests.get(
                article_url,
                headers=header,
                timeout=10
            )
            # Added a timeout to article requests to prevent the scraper from getting stuck.

            article_soup = BeautifulSoup(
                article_response.text,
                "html.parser"
            )

            author_tag = article_soup.find(
                "span",
                class_="Byline-styles__AuthorNameStyled-sc-66f6383-8 YMqIp"
            )

            if author_tag:
                author = author_tag.get_text(strip=True)

        all_news.append({
            "Headline": title,
            "Summary": summary,
            "Link": article_url,
            "Author": author
        })

df = pd.DataFrame(
    all_news,
    columns=["Headline", "Summary", "Link", "Author"]
)

print(f"Total News Scraped: {len(df)}")
# Corrected "Scrapped" to "Scraped" for the correct spelling.

df.to_csv("news_today.csv", index=False)
# Saves the results to a CSV file without adding unnecessary index numbers.