import numpy as np


class Scorer:
    def __init__(self, index, number_of_documents):
        """
        Initializes the Scorer.

        Parameters
        ----------
        index : dict
            The index to score the documents with.
        number_of_documents : int
            The number of documents in the index.
        """

        self.index = index
        self.idf = {}
        self.N = number_of_documents

    def get_list_of_documents(self, query):
        """
        Returns a list of documents that contain at least one of the terms in the query.

        Parameters
        ----------
        query: List[str]
            The query to be scored

        Returns
        -------
        list
            A list of documents that contain at least one of the terms in the query.

        Note
        ---------
            The current approach is not optimal but we use it due to the indexing structure of the dict we're using.
            If we had pairs of (document_id, tf) sorted by document_id, we could improve this.
                We could initialize a list of pointers, each pointing to the first element of each list.
                Then, we could iterate through the lists in parallel.

        """
        list_of_documents = []
        for term in query:
            if term in self.index.keys():
                list_of_documents.extend(self.index[term].keys())
<<<<<<< HEAD:Logic/core/scorer.py
        
        result = list(set(list_of_documents))
        return result
    
=======
        return list(set(list_of_documents))

>>>>>>> template/main:Logic/core/utility/scorer.py
    def get_idf(self, term):
        """
        Returns the inverse document frequency of a term.

        Parameters
        ----------
        term : str
            The term to get the inverse document frequency for.

        Returns
        -------
        float
            The inverse document frequency of the term.

        Note
        -------
            It was better to store dfs in a separate dict in preprocessing.
        """
        idf = self.idf.get(term, None)
        if idf is None:
<<<<<<< HEAD:Logic/core/scorer.py
            N = self.N
            df = len(self.index.get(term, {}))
            idf = np.log(N / df)
            self.idf[term] = idf 
        return idf    
=======
            # TODO
            pass
        return idf
>>>>>>> template/main:Logic/core/utility/scorer.py

    def get_query_tfs(self, query):
        """
        Returns the term frequencies of the terms in the query.

        Parameters
        ----------
        query : List[str]
            The query to get the term frequencies for.

        Returns
        -------
        dict
            A dictionary of the term frequencies of the terms in the query.
        """
<<<<<<< HEAD:Logic/core/scorer.py
        
        terms_tfs = {}
        for term in query:
            term = term.lower()
            terms_tfs[term] = terms_tfs.get(term, 0) + 1
        return terms_tfs
=======
>>>>>>> template/main:Logic/core/utility/scorer.py

        # TODO

    def compute_scores_with_vector_space_model(self, query, method):
        """
        compute scores with vector space model

        Parameters
        ----------
        query: List[str]
            The query to be scored
        method : str ((n|l)(n|t)(n|c).(n|l)(n|t)(n|c))
            The method to use for searching.

        Returns
        -------
        dict
            A dictionary of the document IDs and their scores.
        """
        vect_scores = {}
        query_tfs = self.get_query_tfs(query)
        doc_search_method, query_search_method = method.split('.')
        list_docs = self.get_list_of_documents(query)
        for doc_id in list_docs:
            vect_scores[doc_id] = self.get_vector_space_model_score(query, query_tfs, doc_id, doc_search_method, query_search_method)
        return vect_scores
        pass

    def get_vector_space_model_score(
        self, query, query_tfs, document_id, document_method, query_method
    ):
        """
        Returns the Vector Space Model score of a document for a query.

        Parameters
        ----------
        query: List[str]
            The query to be scored
        query_tfs : dict
            The term frequencies of the terms in the query.
        document_id : str
            The document to calculate the score for.
        document_method : str (n|l)(n|t)(n|c)
            The method to use for the document.
        query_method : str (n|l)(n|t)(n|c)
            The method to use for the query.

        Returns
        -------
        float
            The Vector Space Model score of the document for the query.
        """
        terms = []
        [terms.append(term) for term in query if term not in terms]
        
        query_vactor = []
        doc_vector = []

<<<<<<< HEAD:Logic/core/scorer.py
        doc_tf_method, doc_idf_method, doc_norm_method = document_method
        query_tf_method, query_idf_method, query_norm_method = query_method
        
        for term in terms:
            if term in self.index:

                query_s = 0
                tf = query_tfs[term]
                idf = self.get_idf(term)
                if query_tf_method == 'l':
                    if tf == 0:
                        query_s = 0
                    else:
                        query_s = np.log(tf) + 1
                elif query_tf_method == 'n':
                    query_s = tf
                if query_idf_method == 't':
                    query_s = query_s * idf
                query_vactor.append(query_s)
                

                doc_s = 0
                doc_tf = self.index[term].get(document_id, 0)
                if doc_tf_method == 'l':
                    if doc_tf == 0:
                        doc_s = 0
                    else:
                        doc_s = np.log(doc_tf) + 1
                elif doc_tf_method == 'n':
                    doc_s = doc_tf
                if doc_idf_method == 't':
                    doc_s = doc_s * idf
                doc_vector.append(doc_s)


        if query_norm_method == 'c':
            query_vect = np.array(query_vactor)
            query_norm = np.linalg.norm(query_vect)
            query_vactor = list(query_vect / query_norm)

        if doc_norm_method == 'c':
            doc_vect = np.array(doc_vector)
            doc_norm = np.linalg.norm(doc_vect)
            doc_vector = list(doc_vect / doc_norm)

        return np.dot(np.array(query_vactor), np.array(doc_vector))
=======
        # TODO
>>>>>>> template/main:Logic/core/utility/scorer.py
        pass

    def compute_socres_with_okapi_bm25(
        self, query, average_document_field_length, document_lengths
    ):
        """
        compute scores with okapi bm25

        Parameters
        ----------
        query: List[str]
            The query to be scored
        average_document_field_length : float
            The average length of the documents in the index.
        document_lengths : dict
            A dictionary of the document lengths. The keys are the document IDs, and the values are
            the document's length in that field.

        Returns
        -------
        dict
            A dictionary of the document IDs and their scores.
        """

        doc_scores = {}
        list_of_doc_ids = self.get_list_of_documents(query) 
        for doc_id in list_of_doc_ids:
            doc_scores[doc_id] = self.get_okapi_bm25_score(query, doc_id, average_document_field_length, document_lengths)
        return doc_scores

    def get_okapi_bm25_score(
        self, query, document_id, average_document_field_length, document_lengths
    ):
        """
        Returns the Okapi BM25 score of a document for a query.

        Parameters
        ----------
        query: List[str]
            The query to be scored
        document_id : str
            The document to calculate the score for.
        average_document_field_length : float
            The average length of the documents in the index.
        document_lengths : dict
            A dictionary of the document lengths. The keys are the document IDs, and the values are
            the document's length in that field.

        Returns
        -------
        float
            The Okapi BM25 score of the document for the query.
        """
        k1 = 1.5
        b = 0.75
        okapi_bm25_score = 0.0

<<<<<<< HEAD:Logic/core/scorer.py
        dl = document_lengths.get(document_id, 0)
        for term in query:
            df = len(self.index.get(term, {}))
            
            if df == 0:
                continue

            term_docs = self.index[term]
            tf = term_docs.get(document_id, 0)
            B = (1 - b) + (b * dl/average_document_field_length)
            okapi_tf = ((k1 + 1) * tf) / (k1 * B + tf)
            okapi_idf = np.log(((self.N - df + 0.5) / (df + 0.5)) + 1)
            okapi_bm25_score += okapi_idf * okapi_tf
        
        return okapi_bm25_score
=======
        # TODO
        pass

    def compute_scores_with_unigram_model(
        self, query, smoothing_method, document_lengths=None, alpha=0.5, lamda=0.5
    ):
        """
        Calculates the scores for each document based on the unigram model.

        Parameters
        ----------
        query : str
            The query to search for.
        smoothing_method : str (bayes | naive | mixture)
            The method used for smoothing the probabilities in the unigram model.
        document_lengths : dict
            A dictionary of the document lengths. The keys are the document IDs, and the values are
            the document's length in that field.
        alpha : float, optional
            The parameter used in bayesian smoothing method. Defaults to 0.5.
        lamda : float, optional
            The parameter used in some smoothing methods to balance between the document
            probability and the collection probability. Defaults to 0.5.

        Returns
        -------
        float
            A dictionary of the document IDs and their scores.
        """

        # TODO
        pass

    def compute_score_with_unigram_model(
        self, query, document_id, smoothing_method, document_lengths, alpha, lamda
    ):
        """
        Calculates the scores for each document based on the unigram model.

        Parameters
        ----------
        query : str
            The query to search for.
        document_id : str
            The document to calculate the score for.
        smoothing_method : str (bayes | naive | mixture)
            The method used for smoothing the probabilities in the unigram model.
        document_lengths : dict
            A dictionary of the document lengths. The keys are the document IDs, and the values are
            the document's length in that field.
        alpha : float, optional
            The parameter used in bayesian smoothing method. Defaults to 0.5.
        lamda : float, optional
            The parameter used in some smoothing methods to balance between the document
            probability and the collection probability. Defaults to 0.5.

        Returns
        -------
        float
            The Unigram score of the document for the query.
        """

        # TODO
        pass
>>>>>>> template/main:Logic/core/utility/scorer.py
