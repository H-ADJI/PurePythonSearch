"""
File: indexing.py
File Created: Thursday, 2nd February 2023 4:42:49 pm
Author: KHALIL HADJI 
-----
Copyright:  KHALIL HADJI 2023
"""
import math
from dataclasses import dataclass
from typing import Literal

from search_engine.database import Jobs, get_job_by_id, job_generator

from .data_processing import tokenize
from loguru import logger

@dataclass
class SearchResult:
    relevancy_score: float
    document: Jobs


class SearchEngine:
    """
    Search Engine Dyal Lay7sen L3wan
    """

    def __init__(self):
        """
        inverted_index : an inverted index that map a token to
        the set of all documents ids where the token appears
        documents_index : ids of the indexed documents
        """
        self.inverted_index: dict[str, set] = {}
        self.documents_index: set[int] = set()

    def load_data(self):
        logger.info("STARTING DATA LOADING")
        for job in job_generator():
            self._index_document(job=job)
        logger.info("FINISHED DATA LOADING")

    def _index_document(self, job: Jobs):
        if job.id not in self.documents_index:
            self.documents_index.add(job.id)

        for token in job.clean_tokens:
            if token not in self.inverted_index:
                self.inverted_index[token] = set()
            self.inverted_index[token].add(job.id)

    def _document_frequency(self, token: str) -> int:
        """A measure of abundance :
        Count how many documents contains a specific token


        Args:
            token (str): the token we're looking for

        Returns:
            int: the how many documents contain the token
        """
        return len(self.inverted_index.get(token, set()))

    def _inverse_document_frequency(self, token: str) -> float:
        """Computes the inverse document frequency of a token:
        how many documents we have on our index divided by
        the number of documents that contains the token
        its a kind of popularity measure to decide if the token contributes
        to the special meaning of the document

        Args:
            token (str): a text token

        Returns:
            float: the ratio of the number of documents and the abundance of the token
        """
        return math.log2(
            len(self.documents_index) / (self._document_frequency(token=token) + 1)
        )

    def _results(self, query: list):
        """return a list containing the ids of documents that contains a specific token

        Args:
            parsed_query (list): tokens of the input search query

        Returns:
            list: Documents ids
        """

        return [self.inverted_index.get(token, set()) for token in query]

    def _rank(self, query: list[str], document_ids: list[str]) -> list[SearchResult]:
        """_summary_

        Args:
            parsed_query (list[str]): _description_
            document_ids (list[str]): _description_

        Returns:
            list[SearchResult]: _description_
        """
        results = []
        if not document_ids:
            return results
        for id in document_ids:
            document: Jobs = get_job_by_id(id)

            # calculate score here
            doc_relevancy_score = 0
            for query_term in query:
                tf = document.term_frequency(term=query_term)
                idf = self._inverse_document_frequency(token=query_term)
                doc_relevancy_score += tf * idf
            results.append(
                SearchResult(relevancy_score=doc_relevancy_score, document=document)
            )

        return sorted(results, key=lambda x: x.relevancy_score, reverse=True)

    def search(self, query: str, rank=True, search_type: Literal["AND", "OR"] = "OR"):
        logger.info("STARTING SEARCH")
        parsed_query = tokenize(text=query)
        results = self._results(query=parsed_query)
        if search_type == "AND":
            hits = set.intersection(*results)
        else:
            hits = set.union(*results)
        if rank:
            results = self._rank(query=parsed_query, document_ids=hits)
            for search_result in results:
                yield f" ==> job title : {search_result.document.title} \n ==> SCORE : {search_result.relevancy_score}"  # noqa E501
        else:
            for id in hits:
                yield f" ==> job title : {get_job_by_id(id).title} "  # noqa E501
        logger.info("FINISHED SEARCH")
