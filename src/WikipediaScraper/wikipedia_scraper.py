import re
from collections import defaultdict
from operator import itemgetter

import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from wordcloud import WordCloud


def load_page(url: str) -> list[dict]:
    """Load html content from requested Wikipedia page using Wikipedia's API and separate them into sections.

    Args:
        url (str): URL of requested Wikipedia page to parse

    Returns:
        list[dict]: List of dictionaries. Each dictionary contains
          the parsed plain-text and hyperlinks for the section.
    """
    headers = {
        "User-Agent": "Wikipedia-Scrapper (https://github.com/tibtiq/Wikipedia-Scraper; 29826331+tibtiq@users.noreply.github.com)"
    }

    parsed_sections = []

    # use Wikipedia's API to get page content
    page_name = url.split("/")[-1]

    # get title and index of every section of requested Wikipedia page
    response = requests.get(
        f"https://en.wikipedia.org/w/api.php?action=parse&prop=tocdata&format=json&page={page_name}",
        headers=headers,
    )
    response = response.json()["parse"]["tocdata"]["sections"]
    for section_metadata in response:
        section = dict()
        section["title"] = section_metadata["line"]
        section["index"] = section_metadata["index"]
        parsed_sections.append(section)

    for section in parsed_sections:
        # get html extract of page content from Wikipedia's API
        response = requests.get(
            f"https://en.wikipedia.org/w/api.php?action=parse&section={section['index']}&prop=text&format=json&page={page_name}",
            headers=headers,
        )
        response = response.json()["parse"]["text"]["*"]

        # parse html extract using BeautifulSoup
        parsed_html = BeautifulSoup(response, features="lxml")
        text = []
        hyperlinks = []
        for p in parsed_html.find_all("p"):
            # parse plain-text for each section
            parsed_text = p.getText()
            parsed_text = re.sub(
                r"(\[(.*?)\])+", "", parsed_text
            )  # remove citation tags
            parsed_text = parsed_text.replace(
                "\n", " "
            )  # remove new line character between paragraphs
            parsed_text = parsed_text.replace("'", "'")
            text.append(parsed_text)

            # parse hyperlinks for each section
            for a in p.find_all("a", href=True):
                # avoid citation notes
                path = a["href"]
                if "#cite_note" not in path:
                    hyperlinks.append(path)

        text = "".join(text)
        section["text"] = text

        hyperlinks = [f"https://en.wikipedia.org/{i}" for i in hyperlinks]
        section["hyperlinks"] = hyperlinks

    return parsed_sections


def digest_page(parsed_sections: list[dict]) -> list[dict]:
    """Digest parsed section by removing stop words and punctuation; then computing the frequency
    of words for each section.

    Args:
        parsed_section (list[dict]): List of dictionaries. Each dictionary
          contains the parsed plain-text and hyperlinks for the section.

    Returns:
      list[dict]: List of dictionaries. Each dictionary
        contains the parsed plain-text, hyperlinks for the section, word
          frequencies excluding 'stop words'.
    """

    for section in parsed_sections:
        # tokenize text
        token_list = section["text"].lower().split()

        # remove stop words
        for stop_word in stopwords.words("english"):
            token_list = [token for token in token_list if token != stop_word]

        # remove punctuation
        punctuation = list(".,'\"")
        for i in punctuation:
            token_list = [token.replace(i, "") for token in token_list]

        # compute word frequencies
        word_frequencies = defaultdict(int)
        for token in token_list:
            word_frequencies[token] += 1
        # sort word frequencies in descending order
        word_frequencies = sorted(
            word_frequencies.items(), key=itemgetter(1), reverse=True
        )
        section["frequencies"] = dict(word_frequencies)

    return parsed_sections


if __name__ == "__main__":
    # setup wikipedia link to be scraped
    url = "https://en.wikipedia.org/wiki/google"

    # scrap and parse link
    parsed_sections = load_page(url)
    parsed_sections = digest_page(parsed_sections)
