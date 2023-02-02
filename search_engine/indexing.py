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


@dataclass
class Job():
    id: Optional[str]
    url: Optional[str]
    title: Optional[str]
    description: Optional[str]

    @property
    def clean_tokens(self):
        return full_parse(self.title + " " + self.description)


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

        for token in job.clean_tokens:
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(job.id)

    def _results(self, parsed_query):
        return [self.index.get(token, set()) for token in parsed_query]

    def search(self, query):
        parsed_query = full_parse(text=query)
        results = self._results(parsed_query=parsed_query)
        if results:
            for id in set.intersection(*results):
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
