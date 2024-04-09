class SpellCorrection:
    def __init__(self, all_documents):
        """
        Initialize the SpellCorrection

        Parameters
        ----------
        all_documents : list of str
            The input documents.
        """
        self.all_shingled_words, self.word_counter = self.shingling_and_counting(all_documents)

    def shingle_word(self, word, k=2):
        """
        Convert a word into a set of shingles.

        Parameters
        ----------
        word : str
            The input word.
        k : int
            The size of each shingle.

        Returns
        -------
        set
            A set of shingles.
        """
        shingles = set()
        word_len = len(word)
        for i in range(word_len - k + 1):
            word_to_add = word[i : i + k] 
            shingles.add(word_to_add)

        return shingles
    
    def jaccard_score(self, first_set, second_set):
        """
        Calculate jaccard score.

        Parameters
        ----------
        first_set : set
            First set of shingles.
        second_set : set
            Second set of shingles.

        Returns
        -------
        float
            Jaccard score.
        """
        intersection = len(first_set.intersection(second_set))
        union = len(first_set.union(second_set))

        if union != 0:
            return intersection / union
        return 0.0

    def shingling_and_counting(self, all_documents):
        """
        Shingle all words of the corpus and count TF of each word.

        Parameters
        ----------
        all_documents : list of str
            The input documents.

        Returns
        -------
        all_shingled_words : dict
            A dictionary from words to their shingle sets.
        word_counter : dict
            A dictionary from words to their TFs.
        """
        all_shingled_words = dict()
        word_counter = dict()
        for document in all_documents:
            words = document.split()
            for word in words:
                shingles = self.shingle_word(word)
                all_shingled_words[word] = shingles
                
                if word in word_counter:
                    word_counter[word] += 1
                else:
                    word_counter[word] = 1

        return all_shingled_words, word_counter
    
    def find_nearest_words(self, word):
        """
        Find correct form of a misspelled word.

        Parameters
        ----------
        word : stf
            The misspelled word.

        Returns
        -------
        list of str
            5 nearest words.
        """
        top5_candidates = list()
        jaccard_scores = {}
        input_word_shingles = self.shingle_word(word)
        
        for curr_word, shingles in self.all_shingled_words.items():
            if curr_word != word:
                jaccard_scores[curr_word] = self.jaccard_score(input_word_shingles, shingles)

        sorted_candidates = sorted(jaccard_scores.items(), key=lambda x: x[1], reverse=True)
        candidates = sorted_candidates[:5]
        for candidate, s in candidates:
            top5_candidates.append(candidate)

        return top5_candidates
    
    def spell_check(self, query):
        """
        Find correct form of a misspelled query.

        Parameters
        ----------
        query : stf
            The misspelled query.

        Returns
        -------
        str
            Correct form of the query.
        """
        # TODO Convert the query to lowercase ????????????
        final_result = ""
        words = query.split()
        
        for word in words:
            if word in self.all_shingled_words:
                final_result = final_result + word + " "
            else:
                nearest_words = self.find_nearest_words(word)
                
                if nearest_words:
                    nearest_words_tf = []
                    for n_word in nearest_words:
                        nearest_words_tf.append(self.word_counter[n_word])
                    max_tf = max(nearest_words_tf)
                    
                    scores = []
                    for candidate in nearest_words:
                        jacard = self.jaccard_score(self.shingle_word(word), self.all_shingled_words[candidate])
                        word_tf = self.word_counter[candidate]
                        scores.append((candidate, word_tf / max_tf * jacard))
                
                    best_mach = max(scores, key=lambda x: x[1])[0]
                    final_result = final_result + best_mach + " "
                else:
                    final_result = final_result + word + " " 

        return final_result