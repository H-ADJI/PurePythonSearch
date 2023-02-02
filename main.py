'''
File: main.py
File Created: Thursday, 2nd February 2023 4:42:00 pm
Author: KHALIL HADJI 
-----
Copyright:  KHALIL HADJI 2023
'''

from search_engine.indexing import Index, load_data_to_index


def main():
    jobs_index = Index()
    jobs_index = load_data_to_index(index=jobs_index)
    while True:
        search_query = input("Enter a search query for the job you want\n")
        result_generator = jobs_index.search(search_query)
        value = next(result_generator, None)
        if not value:
            print("no search results\n")
        while value:
            print(value)
            value = next(result_generator, None)
            if not value:
                print("\n no more results \n")
            if input("Press enter to show next result, type 'stop' to cancel search\n") == 'stop':
                break


if __name__ == "__main__":
    main()
