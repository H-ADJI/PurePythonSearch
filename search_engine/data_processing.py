"""
File: data_cleaning.py
File Created: Thursday, 2nd February 2023 4:42:59 pm
Author: KHALIL HADJI 
-----
Copyright:  KHALIL HADJI 2023
"""

import spacy

nlp = spacy.load("en_core_web_sm")


# with open("keywords.txt", "r") as k_f, open("stop_words.txt", "r") as s_f, open(
#     "languages.txt", "r"
# ) as l_f:
#     IT_KEYWORDS = k_f.read().split("\n")
#     PROG_LANGUAGES = l_f.read().split("\n")
#     STOPWORDS = s_f.read().split("\n")


def tokenize(text: str):
    doc = nlp(text)
    return [token.text for token in doc if not token.is_stop and token.is_alpha]
