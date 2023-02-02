'''
File: data_cleaning.py
File Created: Thursday, 2nd February 2023 4:42:59 pm
Author: KHALIL HADJI 
-----
Copyright:  KHALIL HADJI 2023
'''
import time
import re
from collections import Counter
import string
STOPWORDS = set(['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have',
                 'I', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you',
                 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'f', "h"])


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
    return stopword_filter(lower_tokens(tokenize(remove_punctuation(remove_separator(text)))))
