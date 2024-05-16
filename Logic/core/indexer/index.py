from collections import defaultdict
import time
import os
import sys
import json
import copy
from indexes_enum import Indexes
curr_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(curr_dir)
sys.path.append(parent_dir)
from preprocess import Preprocessor
from .indexes_enum import Indexes


class Index:
    def __init__(self, preprocessed_documents: list):
        """
        Create a class for indexing.
        """

        self.preprocessed_documents = preprocessed_documents

        self.index = {
            Indexes.DOCUMENTS.value: self.index_documents(),
            Indexes.STARS.value: self.index_stars(),
            Indexes.GENRES.value: self.index_genres(),
            Indexes.SUMMARIES.value: self.index_summaries(),
        }

    def index_documents(self):
        """
        Index the documents based on the document ID. In other words, create a dictionary
        where the key is the document ID and the value is the document.

        Returns
        ----------
        dict
            The index of the documents based on the document ID.
        """

        current_index = {}
        for document in self.preprocessed_documents:
            doc_id = document['id']
            current_index[doc_id] = document
        return current_index

    def index_stars(self):
        """
        Index the documents based on the stars.

        Returns
        ----------
        dict
            The index of the documents based on the stars. You should also store each terms' tf in each document.
            So the index type is: {term: {document_id: tf}}
        """
        current_index = defaultdict(dict)
        for document in self.preprocessed_documents:
            for star in document['stars']:
                if document['id'] in current_index[star]:
                    current_index[star][document['id']] += 1
                else:
                    current_index[star][document['id']] = 1
        return current_index

    def index_genres(self):
        """
        Index the documents based on the genres.

        Returns
        ----------
        dict
            The index of the documents based on the genres. You should also store each terms' tf in each document.
            So the index type is: {term: {document_id: tf}}
        """
        current_index = defaultdict(dict)
        for document in self.preprocessed_documents:
            for genre in document['genres']:
                if document['id'] in current_index[genre]:
                    current_index[genre][document['id']] += 1
                else:
                    current_index[genre][document['id']] = 1
        return current_index

    def index_summaries(self):
        """
        Index the documents based on the summaries (not first_page_summary).

        Returns
        ----------
        dict
            The index of the documents based on the summaries. You should also store each terms' tf in each document.
            So the index type is: {term: {document_id: tf}}
        """
    
        current_index = defaultdict(dict)
        for document in self.preprocessed_documents:
            for summary in document['summaries']:
                if document['id'] in current_index[summary]:
                    current_index[summary][document['id']] += 1
                else:
                    current_index[summary][document['id']] = 1
        return current_index

    def get_posting_list(self, word: str, index_type: str):
        """
        get posting_list of a word

        Parameters
        ----------
        word: str
            word we want to check
        index_type: str
            type of index we want to check (documents, stars, genres, summaries)

        Return
        ----------
        list
            posting list of the word (you should return the list of document IDs that contain the word and ignore the tf)
        """

        try:
            return list(self.index[index_type][word].keys())
        except KeyError:
            return []

    def add_document_to_index(self, document: dict):
        """
        Add a document to all the indexes

        Parameters
        ----------
        document : dict
            Document to add to all the indexes
        """

        doc_id = document['id']
        self.index[Indexes.DOCUMENTS.value][doc_id] = document

        for index_type in ["stars", "genres"]:
            if index_type in document:
                for term in document[index_type]:
                    if term not in self.index[index_type]:
                        self.index[index_type][term] = {}
                    if doc_id in self.index[index_type][term]:
                        self.index[index_type][term][doc_id] += 1
                    else:
                        self.index[index_type][term][doc_id] = 1
        
        sum_index_type = Indexes.SUMMARIES.value
        if sum_index_type in document:
            for summary in document[sum_index_type]:
                words = summary.split()
                for word in words:
                    if word not in self.index[sum_index_type]:
                        self.index[sum_index_type][word] = {}
                    if doc_id in self.index[sum_index_type][word]:
                        self.index[sum_index_type][word][doc_id] += 1
                    else:
                        self.index[sum_index_type][word][doc_id] = 1
        
    def remove_document_from_index(self, document_id: str):
        """
        Remove a document from all the indexes

        Parameters
        ----------
        document_id : str
            ID of the document to remove from all the indexes
        """
        doc_index = Indexes.DOCUMENTS.value
        if document_id in self.index[doc_index]:
            self.index[doc_index].pop(document_id)
            
        for index_type in [Indexes.STARS.value, Indexes.GENRES.value, Indexes.SUMMARIES.value]:
            terms = list(self.index[index_type].keys())
            for term in terms:
                if document_id in self.index[index_type][term]:
                    self.index[index_type][term].pop(document_id)
        
    def check_add_remove_is_correct(self):
        """
        Check if the add and remove is correct
        """

        dummy_document = {
            'id': '100',
            'stars': ['tim', 'henry'],
            'genres': ['drama', 'crime'],
            'summaries': ['good']
        }

        index_before_add = copy.deepcopy(self.index)
        self.add_document_to_index(dummy_document)
        index_after_add = copy.deepcopy(self.index)

        if index_after_add[Indexes.DOCUMENTS.value]['100'] != dummy_document:
            print('Add is incorrect, document')
            return

        if (set(index_after_add[Indexes.STARS.value]['tim']).difference(set(index_before_add[Indexes.STARS.value]['tim']))
                != {dummy_document['id']}):
            print('Add is incorrect, tim')
            return

        if (set(index_after_add[Indexes.STARS.value]['henry']).difference(set(index_before_add[Indexes.STARS.value]['henry']))
                != {dummy_document['id']}):
            print('Add is incorrect, henry')
            return
        if (set(index_after_add[Indexes.GENRES.value]['drama']).difference(set(index_before_add[Indexes.GENRES.value]['drama']))
                != {dummy_document['id']}):
            print('Add is incorrect, drama')
            return

        if (set(index_after_add[Indexes.GENRES.value]['crime']).difference(set(index_before_add[Indexes.GENRES.value]['crime']))
                != {dummy_document['id']}):
            print('Add is incorrect, crime')
            return

        if (set(index_after_add[Indexes.SUMMARIES.value]['good']).difference(set(index_before_add[Indexes.SUMMARIES.value]['good']))
                != {dummy_document['id']}):
            print('Add is incorrect, good')
            return

        print('Add is correct')

        self.remove_document_from_index('100')
        index_after_remove = copy.deepcopy(self.index)

        if index_after_remove == index_before_add:
            print('Remove is correct')
        else:
            print('Remove is incorrect')

    def store_index(self, path: str, index_name: str = None):
        """
        Stores the index in a file (such as a JSON file)

        Parameters
        ----------
        path : str
            Path to store the file
        index_name: str
            name of index we want to store (documents, stars, genres, summaries)
        """

        if not os.path.exists(path):
            os.makedirs(path)

        if index_name not in self.index:
            raise ValueError('Invalid index type')

        with open(os.path.join(path, f"{index_name}.json"), "w") as f:
            json.dump(self.index[index_name], f)

    def load_index(self, path: str):
        """
        Loads the index from a file (such as a JSON file)

        Parameters
        ----------
        path : str
            Path to load the file
        """
        for index_name in Indexes:
            file_path = os.path.join(path, f'{index_name.value}_index.json')
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    self.index[index_name.value] = json.load(f)
        return  
    def check_if_index_loaded_correctly(self, index_type: str, loaded_index: dict):
        """
        Check if the index is loaded correctly

        Parameters
        ----------
        index_type : str
            Type of index to check (documents, stars, genres, summaries)
        loaded_index : dict
            The loaded index

        Returns
        ----------
        bool
            True if index is loaded correctly, False otherwise
        """

        return self.index[index_type] == loaded_index

    def check_if_indexing_is_good(self, index_type: str, check_word: str = 'good'):
        """
        Checks if the indexing is good. Do not change this function. You can use this
        function to check if your indexing is correct.

        Parameters
        ----------
        index_type : str
            Type of index to check (documents, stars, genres, summaries)
        check_word : str
            The word to check in the index

        Returns
        ----------
        bool
            True if indexing is good, False otherwise
        """

        # brute force to check check_word in the summaries
        start = time.time()
        docs = []
        for document in self.preprocessed_documents:
            if index_type not in document or document[index_type] is None:
                continue

            for field in document[index_type]:
                if check_word in field:
                    docs.append(document['id'])
                    break

            # if we have found 3 documents with the word, we can break
            if len(docs) == 3:
                break

        end = time.time()
        brute_force_time = end - start

        # check by getting the posting list of the word
        start = time.time()
        # TODO: based on your implementation, you may need to change the following line
        posting_list = self.get_posting_list(check_word, index_type)

        end = time.time()
        implemented_time = end - start

        print('Brute force time: ', brute_force_time)
        print('Implemented time: ', implemented_time)

        if set(docs).issubset(set(posting_list)):
            print('Indexing is correct')

            if implemented_time < brute_force_time:
                print('Indexing is good')
                return True
            else:
                print('Indexing is bad')
                return False
        else:
            print('Indexing is wrong')
            return False

# TODO: Run the class with needed parameters, then run check methods and finally report the results of check methods

file_path = os.path.abspath("./IMDB_crawled.json")
with open(file_path, "r") as f:
    imdb_data = json.load(f)

ids_list = []
stars_list = []
genres_list = []
summareis_list = []
for movie in imdb_data:
    if (movie['stars'] != 'No stars') and (movie['genres'] != 'No generes') and (movie['summaries'] != 'No summary'):
        ids_list.append(movie['id'])
        stars_list.append(' '.join(movie['stars']))
        genres_list.append(' '.join(movie['genres']))
        summareis_list.append(' '.join(movie['summaries']))

pre2 = Preprocessor(stars_list)
preprocessed_stars = pre2.preprocess()
pre3 = Preprocessor(genres_list)
preprocessed_genres = pre3.preprocess()
pre1 = Preprocessor(summareis_list)
preprocessed_summaries = pre1.preprocess()

pre_docs = []
num_movies = len(ids_list)
for i in range(num_movies):
    movie = {
        'id':ids_list[i],
        'stars':preprocessed_stars[i],
        'genres':preprocessed_genres[i],
        'summaries':preprocessed_summaries[i]
    }
    pre_docs.append(movie)

index = Index(preprocessed_documents=pre_docs)

index.check_add_remove_is_correct()

index.check_if_indexing_is_good('stars', 'Henry')
index.check_if_indexing_is_good('genres', 'drama')
index.check_if_indexing_is_good('summaries', 'good')

index.store_index('indexes', 'documents')
index.store_index('indexes', 'stars')
index.store_index('indexes', 'genres')
index.store_index('indexes', 'summaries')


doc_stat = index.check_if_index_loaded_correctly('documents', index.index['documents'])
stars_stat = index.check_if_index_loaded_correctly('stars', index.index['stars'])
genres_stat = index.check_if_index_loaded_correctly('genres', index.index['genres'])
summaries_stat = index.check_if_index_loaded_correctly('summaries', index.index['summaries'])

print(f'documents loaded: {doc_stat}')
print(f'stars loaded: {stars_stat}')
print(f'genres loaded: {genres_stat}')
print(f'summaries loaded: {summaries_stat}')
