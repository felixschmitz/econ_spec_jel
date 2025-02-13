"""Helper module for data scraping."""

from typing import Any

import requests
from bs4 import BeautifulSoup


def extract_metadata(response: requests.Response, dp_number: int) -> dict[str, Any]:
    """Extract metadata from the response of a discussion paper page.

    Args:
        response (requests.Response): Response object of the discussion paper page.
        dp_number (int): Discussion paper number.

    Returns
    -------
        dict: Metadata.
    """
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.select_one('meta[property="og:title"]')["content"].strip()
    pub_date = soup.select_one("div.publications-header p").text.strip()
    pub_month, pub_year = pub_date.split(" ")
    authors_information = soup.select("div.authors a")
    published = soup.select_one("div.publications-header p").text.strip()
    author_names = [a.text.strip() for a in authors_information]
    author_urls = [a["href"] for a in authors_information]
    abstract = soup.select_one("div.element-copyexpandable p").text.strip()
    keywords = [
        li.text.strip()
        for h3 in soup.find_all("h3", class_="box-list-headline")
        if "Keywords" in h3.text
        for li in h3.find_next("ul").find_all("li")
    ]
    jel_codes = [
        li.text.strip()
        for h3 in soup.find_all("h3", class_="box-list-headline")
        if "JEL Codes" in h3.text
        for li in h3.find_next("ul").find_all("li")
    ]
    try:
        file_url = soup.select_one("a.download-link")["href"]
    except TypeError:
        file_url = None
    return {
        "dp_number": dp_number,
        "title": title,
        "author_names": author_names,
        "author_urls": author_urls,
        "published": published,
        "publication_date_month": pub_month,
        "publication_date_year": pub_year,
        "abstract": abstract,
        "keywords": keywords,
        "jel_codes": jel_codes,
        "file_url": file_url,
    }
