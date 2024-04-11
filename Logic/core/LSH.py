import numpy as np
import itertools
import random


class MinHashLSH:
    def __init__(self, documents, num_hashes):
        """
        Initialize the MinHashLSH

        Parameters
        ----------
        documents : list of str
            The input documents for similarity analysis.
        num_hashes : int
            Number of hashes for mini-hashing.
        """
        self.documents = documents
        self.num_hashes = num_hashes

        # TODO
        # newwwwwwwwwwwwwww
        # self.shingled_documents = self.shingle_documents()

    def shingle_document(self, document, k=2):
        """
        Convert a document into a set of shingles.

        Parameters
        ----------
        document : str
            The input document.
        k : int
            The size of each shingle.

        Returns
        ----------
        set
            A set of shingles.
        """
        # TODO set?
        # TODO spaces?
        document = document.lower()
        shingles = set()

        chars = [char for char in document]

        for i in range(len(chars) - k + 1):
            shingle = ''.join(chars[i : i + k])
            shingles.add(shingle)
        return shingles

    def build_characteristic_matrix(self):
        """
        Build the characteristic matrix representing the presence of shingles in documents.

        Returns
        ----------
        numpy.ndarray
            The binary characteristic matrix.
        """
        all_shingles = set()
        all_docs = self.documents
        docs_shingles = []

        for document in all_docs:
            shingles = self.shingle_document(document)
            docs_shingles.append(list(shingles))
            all_shingles.update(shingles)
        
        doc_num = len(all_docs)
        shingle_num = len(all_shingles)
        characteristic_matrix = np.zeros((doc_num, shingle_num), dtype=int)
        
        shingles_index = {}
        for idx, shingle in enumerate(all_shingles):
            shingles_index[shingle] = idx
        
        for doc_idx in range(len(all_docs)):
            # shingles = self.shingle_document(document)
            shingles = docs_shingles[doc_idx]
            for shingle in shingles:
                characteristic_matrix[doc_idx, shingles_index[shingle]] = 1
        
        return characteristic_matrix

    def min_hash_signature(self):
        """
        Perform Min-Hashing to generate hash signatures for documents.

        Returns
        ----------
        numpy.ndarray
            The Min-Hash signatures matrix.
        """
        characteristic_matrix = self.build_characteristic_matrix()
        doc_num, shingle_num = characteristic_matrix.shape
        signature_matrix = np.full((self.num_hashes, doc_num), np.inf)
        
        permutations = [np.random.permutation(shingle_num) for _ in range(self.num_hashes)]
        for permutation_idx, permutation in enumerate(permutations):
            for doc_idx in range(doc_num):
                for i in range(shingle_num):
                    idx = np.where(permutation == i)[0][0]
                    if characteristic_matrix[doc_idx, idx] == 1: 
                        signature_matrix[permutation_idx, doc_idx] = i  
                        break
        
        return signature_matrix

    def lsh_buckets(self, signature, bands=10, rows_per_band=10):
        """
        Group documents into Locality-Sensitive Hashing (LSH) buckets based on Min-Hash signatures.

        Parameters
        ----------
        signature : numpy.ndarray
            Min-Hash signatures for documents.
        bands : int
            Number of bands for LSH.
        rows_per_band : int
            Number of rows per band.

        Returns
        ----------
        dict
            A dictionary mapping bucket IDs to lists of document indices.
        """
        # TODO
        _, num_docs = signature.shape
        
        buckets = {}
        
        for band_idx in range(bands):
            band_start = band_idx * rows_per_band
            band_end = (band_idx + 1) * rows_per_band
            band_hashes = signature[band_start:band_end, :]  # Get the band from the signature matrix
            
            # Hash the band portion of each column to a hash table with k buckets
            hash_table = {}
            for doc_idx in range(num_docs):
                band_hash = hash(tuple(band_hashes[:, doc_idx]))
                if band_hash in hash_table:
                    hash_table[band_hash].append(doc_idx)
                else:
                    hash_table[band_hash] = [doc_idx]
            
            # Make k as large as possible
            for bucket_id, docs in hash_table.items():
                if bucket_id not in buckets:
                    buckets[bucket_id] = []
                buckets[bucket_id].extend(docs)
        # print(buckets)
        return buckets

    def perform_lsh(self):
        """
        Perform the entire Locality-Sensitive Hashing (LSH) process.

        Returns
        ----------
        dict
            A dictionary mapping bucket IDs to lists of document indices.
        """
        # TODO
        return

    def jaccard_score(self, first_set, second_set):
        """
        Calculate jaccard score for two sets.

        Parameters
        ----------
        first_set : set
            Set of first shingled document.
        second_set : set
            Set of second shingled document.

        Returns
        ----------
        float
            Jaccard score.
        """
        # TODO
        pass

    def jaccard_similarity_test(self, buckets, all_documents):
        """
        Test your near duplicate detection code based on jaccard similarity.

        Parameters
        ----------
        buckets : dict
            A dictionary mapping bucket IDs to lists of document indices.
        all_documents : list
            The input documents for similarity analysis.
        """
        correct_near_duplicates = 0
        all_near_duplicates = 0

        for bucket_id in buckets.keys():
            docs_in_this_bucket = buckets[bucket_id]
            unique_doc_ids = set(docs_in_this_bucket)
            if len(unique_doc_ids) > 1:
                combinations = list(itertools.combinations(unique_doc_ids, 2))
                for comb in combinations:
                    all_near_duplicates += 1

                    first_doc_id = comb[0]
                    second_doc_id = comb[1]

                    first_shingled_doc = self.shingle_document(all_documents[first_doc_id], 2)
                    second_shingled_doc = self.shingle_document(all_documents[second_doc_id], 2)

                    near_duplicated_jaccard_score = self.jaccard_score(first_shingled_doc, second_shingled_doc)
                    current_score = 0

                    for _ in range(5):
                        random_doc_id = first_doc_id
                        while random_doc_id == first_doc_id or random_doc_id == second_doc_id:
                            random_doc_id = random.randint(0, len(all_documents) - 1)
                        random_shingled_doc = self.shingle_document(all_documents[random_doc_id], 2)

                        random_jaccard_score = self.jaccard_score(first_shingled_doc, random_shingled_doc)

                        if near_duplicated_jaccard_score > random_jaccard_score:
                            current_score += 1

                    if current_score == 5:
                        correct_near_duplicates += 1

        # a good score is around 0.8
        print("your final score in near duplicate detection:", correct_near_duplicates / all_near_duplicates)
