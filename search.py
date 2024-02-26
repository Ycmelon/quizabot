import cloudscraper
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()


def get_answer_ddg(query: str) -> str:
    r = scraper.get(f"https://html.duckduckgo.com/html?q={quote_plus(query)}")
    soup = BeautifulSoup(r.text, features="lxml")

    elements = soup.select("h2.result__title, a.result__snippet")
    result = "".join(element.text for element in elements)

    if "confirm this search was made by a human" in soup.text:
        raise Exception("Search failed due to human verification")

    return result[:1000]


def get_answer_google(query: str) -> str:
    r = scraper.get(f"https://www.google.com/search?q={quote_plus(query)}")
    soup = BeautifulSoup(r.text, features="lxml")

    result = soup.select_one("div#main")
    if result is None:
        raise Exception("Unknown error")

    return result.text[:1000]


get_answer = get_answer_google  # by default, use google
