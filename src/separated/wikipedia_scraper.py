import requests
import re
from bs4 import BeautifulSoup
from typing import List, Dict
from collections import defaultdict
from operator import itemgetter
import matplotlib.pyplot as plt

# use nltk for list of stop words
import nltk

nltk.download("stopwords")
from nltk.corpus import stopwords
from wordcloud import WordCloud


def load_page(url: str) -> List[dict]:
    """
    Load html content from requested Wikipedia page using
    Wikipedia's API and separate them into sections.

    Args:
        url (str): URL of requested Wikipedia page to parse

    Returns:
        List[dict]: List of dictionaries. Each dictionary contains
          the parsed plain-text and hyperlinks for the section.
    """

    parsed_sections = []

    # use Wikipedia's API to get page content
    page_name = url.split("/")[-1]

    # get title and index of every section of requested Wikipedia page
    response = requests.get(
        f"https://en.wikipedia.org/w/api.php?action=parse&prop=sections&format=json&page={page_name}"
    )
    response = response.json()["parse"]["sections"]
    for section_metadata in response:
        section = dict()
        section["title"] = section_metadata["line"]
        section["index"] = section_metadata["index"]
        parsed_sections.append(section)

    for section in parsed_sections:
        # get html extract of page content from Wikipedia's API
        response = requests.get(
            f"https://en.wikipedia.org/w/api.php?action=parse&section={section['index']}&prop=text&format=json&page={page_name}"
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


def digest_page(parsed_sections: List[Dict]) -> List[Dict]:
    """
    Digest parsed section by removing stop words and punctuation; then computing
    the frequency of words for each section.

    Args:
        parsed_section (List[Dict]): List of dictionaries. Each dictionary
          contains the parsed plain-text and hyperlinks for the section.

    Returns:
      List[Dict]: List of dictionaries. Each dictionary
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


def display_piecharts(
    parsed_sections: List[Dict],
    frequency_cutoff: int = 0,
    group_below_cutoff: bool = False,
    remove_below_cutoff: bool = False,
    num_sections_to_show: int = 5,
) -> None:
    """
    Displays parsed information from Wikipedia page in a pie chart using given
    specifications.

    Args:
        parsed_sections (List[Dict]): List of dictionaries. Each dictionary
          contains the parsed plain-text and hyperlinks for the section.
        frequency_cutoff (int): Value used to determine how to remove or group
          words words based on their frequency. Defaults to 0.
        group_below_cutoff (bool): Specifies whether or not to group words that
          have frequencies that are equal to or below the cutoff value into a
          single group. Defaults to False.
        remove_below_cutoff (bool): Specifies whether or not to remove words
          that have frequencies that are equal to or below the cutoff value.
          Defaults to False.
        num_sections_to_show (int): Specifies the number of sections to display
          graphs for. Defaults to 5.

    Returns:
      None
    """

    for section in parsed_sections[:num_sections_to_show]:
        word_frequencies = dict(section["frequencies"].items())

        # find words with frequencies below frequency_cutoff
        if frequency_cutoff != 0:
            words_below_cutoff = [
                token
                for token in word_frequencies.items()
                if token[1] <= frequency_cutoff
            ]

            # remove words with frequencies below frequency_cutoff
            if remove_below_cutoff or group_below_cutoff:
                # combine words with frequencies below frequency_cutoff into one group
                if group_below_cutoff:
                    word_frequencies["grouped_words"] = sum(
                        [token[1] for token in words_below_cutoff]
                    )

                for key, _ in words_below_cutoff:
                    del word_frequencies[key]

        # compute percentages to display on pie chart
        total_words = sum(word_frequencies.values())
        for word in word_frequencies:
            word_frequencies[word] = (word_frequencies[word] / total_words) * 100

        # graph pie chart
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 2, 2])
        ax.pie(
            word_frequencies.values(), labels=word_frequencies.keys(), autopct="%1.1f%%"
        )
        ax.set_title(f'Section: {section["title"]}')
        plt.show()


def display_barcharts(
    parsed_sections: List[Dict],
    frequency_cutoff: int = 0,
    group_below_cutoff: bool = False,
    remove_below_cutoff: bool = False,
    num_sections_to_show: int = 5,
) -> None:
    """
    Displays parsed information from Wikipedia page in a bar chart using given
    specifications.

    Args:
        parsed_sections (List[Dict]): List of dictionaries. Each dictionary
          contains the parsed plain-text and hyperlinks for the section.
        frequency_cutoff (int): Value used to determine how to remove or group
          words words based on their frequency. Defaults to 0.
        group_below_cutoff (bool): Specifies whether or not to group words that
          have frequencies that are equal to or below the cutoff value into a
          single group. Defaults to False.
        remove_below_cutoff (bool): Specifies whether or not to remove words
          that have frequencies that are equal to or below the cutoff value.
          Defaults to False.
        num_sections_to_show (int): Specifies the number of sections to display
          graphs for. Defaults to 5.

    Returns:
      None
    """

    for section in parsed_sections[:num_sections_to_show]:
        word_frequencies = dict(section["frequencies"].items())

        # find words with frequencies below frequency_cutoff
        if frequency_cutoff != 0:
            words_below_cutoff = [
                token
                for token in word_frequencies.items()
                if token[1] <= frequency_cutoff
            ]

            # remove words with frequencies below frequency_cutoff
            if remove_below_cutoff or group_below_cutoff:
                # combine words with frequencies below frequency_cutoff into one group
                if group_below_cutoff:
                    word_frequencies["grouped_words"] = sum(
                        [token[1] for token in words_below_cutoff]
                    )

                for key, _ in words_below_cutoff:
                    del word_frequencies[key]

        # graph bar chart
        fig = plt.figure(figsize=(15, 4.8))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(word_frequencies.keys(), word_frequencies.values())
        ax.set_title(f'Section: {section["title"]}')
        plt.show()


def display_wordclouds(
    parsed_sections: List[Dict],
    frequency_cutoff: int = 0,
    group_below_cutoff: bool = False,
    remove_below_cutoff: bool = False,
    num_sections_to_show: int = 5,
) -> None:
    """
    Displays parsed information from Wikipedia page in a word cloud using given
    specifications.

    Args:
        parsed_sections (List[Dict]): List of dictionaries. Each dictionary
          contains the parsed plain-text and hyperlinks for the section.
        frequency_cutoff (int): Value used to determine how to remove or group
          words words based on their frequency. Defaults to 0.
        group_below_cutoff (bool): Specifies whether or not to group words that
          have frequencies that are equal to or below the cutoff value into a
          single group. Defaults to False.
        remove_below_cutoff (bool): Specifies whether or not to remove words
          that have frequencies that are equal to or below the cutoff value.
          Defaults to False.
        num_sections_to_show (int): Specifies the number of sections to display
          graphs for. Defaults to 5.

    Returns:
      None
    """

    for section in parsed_sections[:num_sections_to_show]:
        word_frequencies = dict(section["frequencies"].items())

        # find words with frequencies below frequency_cutoff
        if frequency_cutoff != 0:
            words_below_cutoff = [
                token
                for token in word_frequencies.items()
                if token[1] <= frequency_cutoff
            ]

            # remove words with frequencies below frequency_cutoff
            if remove_below_cutoff or group_below_cutoff:
                # combine words with frequencies below frequency_cutoff into one group
                if group_below_cutoff:
                    word_frequencies["grouped_words"] = sum(
                        [token[1] for token in words_below_cutoff]
                    )

                for key, _ in words_below_cutoff:
                    del word_frequencies[key]

        section_text = []
        for word, freq in word_frequencies.items():
            for f in range(freq):
                section_text.append(word)
        section_text = " ".join(section_text)

        # generate WordCloud image
        wordcloud = WordCloud(
            width=800, height=800, background_color="white", min_font_size=10
        ).generate(section_text)

        # plot the WordCloud image
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.title(f'Section: {section["title"]}')
        plt.imshow(wordcloud)

        plt.axis("off")
        plt.tight_layout(pad=0)

        plt.show()


def display_rawdata(parsed_sections: List[Dict], num_sections_to_show: int = 5) -> None:
    """
    Displays parsed information from Wikipedia page.

    Args:
        parsed_sections (List[Dict]): List of dictionaries. Each dictionary
          contains the parsed plain-text and hyperlinks for the section.
        num_sections_to_show (int): Specifies the number of sections to display
          graphs for. Defaults to 5.

    Returns:
      None
    """

    for section in parsed_sections[:num_sections_to_show]:
        print(f"Section: {section['title']}")
        print(f"Word frequencies for section: {section['title']}")
        for word, freq in section["frequencies"].items():
            print(f"\t{word} - {freq}")
        print(f"Hyperlinks for section: {section['title']}")
        for i in section["hyperlinks"]:
            print(f"\t{i}")
        print()


if __name__ == "__main__":
    # setup wikipedia link to be scraped
    url = "https://en.wikipedia.org/wiki/google"

    # scrap and parse link
    parsed_sections = load_page(url)
    parsed_sections = digest_page(parsed_sections)

    display_rawdata(parsed_sections, num_sections_to_show=5)
