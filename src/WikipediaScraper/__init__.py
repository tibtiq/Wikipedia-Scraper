import os
import ssl

import nltk

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


def ensure_nltk_resources():
    venv_base = os.environ.get("VIRTUAL_ENV")
    if venv_base:
        download_dir = os.path.join(venv_base, "share", "nltk_data")
        if download_dir not in nltk.data.path:
            nltk.data.path.append(download_dir)
    else:
        download_dir = None

    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords", download_dir=download_dir)


ensure_nltk_resources()
