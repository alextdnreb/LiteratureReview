import requests
import xml.etree.ElementTree as ET
import pandas as pd
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import re


def query_dblp_api(searchterm: str) -> str:
    """search for a given term via dblp API"""
    urlencoded_searchterm = quote_plus(searchterm)
    return requests.get(
        f"https://dblp.org/search/publ/api?q={urlencoded_searchterm}&h=10000&c=1000"
    )


def retrieve_data_from_dblp_response(response: str) -> pd.DataFrame:
    """
    input: xml from dblp API response as string
    output: DataFrame containing relevant information about papers
    """
    result = pd.DataFrame(columns=["title", "authors", "venue", "year", "doi"])

    root = ET.fromstring(response.text)
    hits = root.find("hits")

    # iterate over search results
    for paper in hits.findall("hit"):
        authors = []
        info = paper.find("info")
        venue = info.find("venue").text if info.find("venue") != None else None
        if info.find("authors") != None:
            for author in info.find("authors"):
                authors.append(author.text)
        title = info.find("title").text if info.find("title") != None else None
        year = info.find("year").text if info.find("year") != None else None
        doi = info.find("doi").text if info.find("doi") != None else None

        row = pd.DataFrame(
            {
                "title": [title],
                "authors": [", ".join(authors)],
                "venue": [venue],
                "year": [year],
                "doi": [doi],
            }
        )

        result = pd.concat([result, row])

    return result


def find_conference_rank(venue: str):
    """search for the rank of a venue on CORE"""
    search_page_url = f"https://portal.core.edu.au/conf-ranks/?search={venue}&by=all&source=CORE2023&sort=atitle&page=1"
    search_page = requests.get(search_page_url)
    if search_page.status_code == 200:
        bs = BeautifulSoup(search_page.content, "html.parser")
        search_results = bs.find_all(string=re.compile(r"\b%s\b" % venue))

        if len(search_results) > 0:
            return search_results[-1].find_next("td").find_next("td").string.strip()
    else:
        return "Z"
