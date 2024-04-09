class Snippet:
    def __init__(self, number_of_words_on_each_side=5):
        """
        Initialize the Snippet

        Parameters
        ----------
        number_of_words_on_each_side : int
            The number of words on each side of the query word in the doc to be presented in the snippet.
        """
        self.number_of_words_on_each_side = number_of_words_on_each_side

    def remove_stop_words_from_query(self, query):
        """
        Remove stop words from the input string.

        Parameters
        ----------
        query : str
            The query that you need to delete stop words from.

        Returns
        -------
        str
            The query without stop words.
        """

        with open('stopwords.txt', 'r') as f:
            stop_words = set(f.read().split())
        
        query_words = query.split()
        modified_query = []
        for word in query_words:
            if word.lower() not in stop_words:
                modified_query.append(word)

        final_query = ' '.join(modified_query)
        return final_query

    def find_snippet(self, doc, query):
        """
        Find snippet in a doc based on a query.

        Parameters
        ----------
        doc : str
            The retrieved doc which the snippet should be extracted from that.
        query : str
            The query which the snippet should be extracted based on that.

        Returns
        -------
        final_snippet : str
            The final extracted snippet. IMPORTANT: The keyword should be wrapped by *** on both sides.
            For example: Sahwshank ***redemption*** is one of ... (for query: redemption)
        not_exist_words : list
            Words in the query which don't exist in the doc.
        """
        # TODO "..." OR " ... "
        final_snippet = ""
        not_exist_words = []

        query_without_stop_words = self.remove_stop_words_from_query(query)
        query_tokens = query_without_stop_words.split()

        s_doc_words = doc.split()
        lower_doc = doc.lower()

        for token in query_tokens:
            lower_token = token.lower()
            if lower_token not in lower_doc:
                not_exist_words.append(token)
                continue
            
            doc_words = lower_doc.split()
            index = None
            for i, word in enumerate(s_doc_words):
                if lower_token == word.lower():
                    word_in_doc = word
                    index = i
                    break
            
            if index is not None:
                start_index = max(0, index - self.number_of_words_on_each_side)
                end_index = min(index + self.number_of_words_on_each_side + 1, len(doc_words))
                
                words_before = s_doc_words[start_index:index]
                words_after = s_doc_words[index + 1:end_index]

                if words_before:
                    final_snippet +=  " " + " ".join(words_before)
                final_snippet += " " + f'***{word_in_doc}***' + " "
                if words_after:
                    final_snippet += " ".join(words_after)
            else:
                not_exist_words.append(token)
        
        if final_snippet:
            words = final_snippet.split()
            final_snippet = " ... ".join(words)

        return final_snippet, not_exist_words