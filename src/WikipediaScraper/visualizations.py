import matplotlib.pyplot as plt
from wordcloud import WordCloud


def display_piecharts(
    parsed_sections: list[dict],
    frequency_cutoff: int = 0,
    group_below_cutoff: bool = False,
    remove_below_cutoff: bool = False,
    num_sections_to_show: int = 5,
) -> None:
    """
    Displays parsed information from Wikipedia page in a pie chart using given
    specifications.

    Args:
        parsed_sections (list[dict]): List of dictionaries. Each dictionary
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
        ax.set_title(f"Section: {section['title']}")
        plt.show()


def display_barcharts(
    parsed_sections: list[dict],
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
        ax.set_title(f"Section: {section['title']}")
        plt.show()


def display_wordclouds(
    parsed_sections: list[dict],
    frequency_cutoff: int = 0,
    group_below_cutoff: bool = False,
    remove_below_cutoff: bool = False,
    num_sections_to_show: int = 5,
) -> None:
    """
    Displays parsed information from Wikipedia page in a word cloud using given
    specifications.

    Args:
        parsed_sections (list[dict]): List of dictionaries. Each dictionary
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
        plt.title(f"Section: {section['title']}")
        plt.imshow(wordcloud)

        plt.axis("off")
        plt.tight_layout(pad=0)

        plt.show()


def display_rawdata(parsed_sections: list[dict], num_sections_to_show: int = 5) -> None:
    """
    Displays parsed information from Wikipedia page.

    Args:
        parsed_sections (list[dict]): List of dictionaries. Each dictionary
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
