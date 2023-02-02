'''
File: indexing.py
File Created: Thursday, 2nd February 2023 4:42:49 pm
Author: KHALIL HADJI 
-----
Copyright:  KHALIL HADJI 2023
'''
from .data_cleaning import full_parse, remove_separator, remove_punctuation
from dataclasses import dataclass
from typing import Optional
from collections import Counter


@dataclass
class Job():
    id: Optional[str]
    url: Optional[str]
    title: Optional[str]
    description: Optional[str]

    @property
    def clean_tokens(self):
        return full_parse(self.title + " " + self.description)

    def generate_counter_bag(self):
        self.bag_of_words = Counter(self.clean_tokens)

    def term_frequency(self, term):
        return self.bag_of_words.get(term, 0)


class Index:
    def __init__(self):
        """ 
        index : is an inverted index that will map a token to the set of all documents id where the token appears
        documents : mapping ids to job documents
        """
        self.index: dict[str, set] = {}
        self.documents: dict[str, Job] = {}

    def index_document(self, job: Job):
        if job.id not in self.documents:
            self.documents[job.id] = job
            job.generate_counter_bag()

        for token in job.clean_tokens:
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(job.id)

    def _results(self, parsed_query):
        return [self.index.get(token, set()) for token in parsed_query]

    def _rank(self, parsed_query: list[str], document_ids: list[str]):
        ranked_results = []
        if not document_ids:
            return ranked_results
        for id in document_ids:
            relevance_score = sum([self.documents.get(id).term_frequency(
                term=query_term) for query_term in parsed_query])
            ranked_results.append((id, relevance_score))
        return sorted(ranked_results, key=lambda x: x[1], reverse=True)

    def search(self, query, rank=True):
        parsed_query = full_parse(text=query)
        results = self._results(parsed_query=parsed_query)
        if results:
            hits = set.intersection(*results)
            if rank:
                results = self._rank(parsed_query=parsed_query,
                                     document_ids=hits)
                for id in hits:
                    yield f" ==> job title : {self.documents.get(id).title} \n ==> job url : {self.documents.get(id).url} \n "
            else:
                for id in hits:
                    yield f" ==> job title : {self.documents.get(id).title} \n ==> job url : {self.documents.get(id).url} \n "


def load_data_to_index(index: Index, file_path: str = "job_details.csv"):
    """
    sample data adapte the data class according to the data you're using
    """
    with open("job_details.csv", 'r') as jobs_file:
        jobs_file.readline()
        while line := jobs_file.readline():
            data_list = line.split("~")

            data = {
                "id": data_list[0],
                "title": data_list[8],
                "description": data_list[1],
                "url": data_list[9]
            }
            job = Job(**data)
            index.index_document(job)
    return index
