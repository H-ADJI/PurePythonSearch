"""
File: data_cleaning.py
File Created: Thursday, 2nd February 2023 4:42:59 pm
Author: KHALIL HADJI 
-----
Copyright:  KHALIL HADJI 2023
"""
import re
import string

with open("keywords.txt", "r") as k_f, open("stop_words.txt", "r") as s_f, open(
    "languages.txt", "r"
) as l_f:
    IT_KEYWORDS = k_f.read().split("\n")
    PROG_LANGUAGES = l_f.read().split("\n")
    STOPWORDS = s_f.read().split("\n")


def remove_separator(text: str, sep: str = "|=|"):
    return text.replace(sep, " ")


def remove_punctuation(text: str):
    # replace punctuation with space
    puctuation = "·…" + string.punctuation
    text = re.sub(rf"[{puctuation}]", " ", text)
    text = re.sub(r"[\n\r]", " ", text)

    # remove repeated spaces
    text = re.sub(r"\s{2,}", " ", text)
    return text


def tokenize(text: str):
    return [t for t in text.split(" ") if t != ""]


def lower_tokens(tokens: list[str]):
    return [token.lower() for token in tokens]


def stopword_filter(tokens):
    return [token for token in tokens if token not in STOPWORDS]


def full_parse(text: str):
    return stopword_filter(
        lower_tokens(tokenize(remove_punctuation(remove_separator(text))))
    )
