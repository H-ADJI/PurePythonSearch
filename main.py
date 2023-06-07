"""
File: main.py
File Created: Thursday, 2nd February 2023 4:42:00 pm
Author: KHALIL HADJI 
-----
Copyright:  KHALIL HADJI 2023
"""
from loguru import logger

from search_engine.indexing import SearchEngine


def main():
    engine = SearchEngine()
    logger.info("Loading data Begin")
    engine.load_data()
    logger.info("Loading data End")
    for result in engine.search(query="python research admin"):
        logger.info(result)


if __name__ == "__main__":
    main()
