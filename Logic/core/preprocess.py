import os
import re
import json
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

class Preprocessor:

    def __init__(self, documents: list):
        """
        Initialize the class.

        Parameters
        ----------
        documents : list
            The list of documents to be preprocessed, path to stop words, or other parameters.
        """
        # TODO
        self.documents = documents        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        stopwords_path = os.path.join(script_dir, "stopwords.txt")
        with open(stopwords_path, "r") as file:
            self.stopwords = set(word.strip() for word in file)

    def preprocess(self):
        """
        Preprocess the text using the methods in the class.

        Returns
        ----------
        List[str]
            The preprocessed documents.
        """
        # TODO
        preprocessed_doc = []
        for document in self.documents:
            preprocessed_1 = self.normalize(document)
            preprocessed_2 = self.remove_links(preprocessed_1)
            preprocessed_3 = self.remove_punctuations(preprocessed_2)
            preprocessed_4 = self.remove_stopwords(preprocessed_3)
            preprocessed_doc.append(preprocessed_4)
        return preprocessed_doc

    def normalize(self, text: str):
        """
        Normalize the text by converting it to a lower case, stemming, lemmatization, etc.

        Parameters
        ----------
        text : str
            The text to be normalized.

        Returns
        ----------
        str
            The normalized text.
        """
        # TODO
        lower_text = text.lower()
        processed_words = []
        stemmer = PorterStemmer()
        text_words = lower_text.split()

        for word in text_words:
            new_word = stemmer.stem(word)
            processed_words.append(new_word)
        normalized_text = ' '.join(processed_words)

        # lower_text = text.lower()
        # processed_words = []
        # tokens = word_tokenize(lower_text)
        # lemmatizer = WordNetLemmatizer()

        # for token in tokens:
        #     lem = lemmatizer.lemmatize(token)
        #     processed_words.append(lem)

        # normalized_text = ' '.join(processed_words)

        return normalized_text

    def remove_links(self, text: str):
        """
        Remove links from the text.

        Parameters
        ----------
        text : str
            The text to be processed.

        Returns
        ----------
        str
            The text with links removed.
        """
        patterns = [r'\S*http\S*', r'\S*www\S*', r'\S+\.ir\S*', r'\S+\.com\S*', r'\S+\.org\S*', r'\S*@\S*']
        # TODO
        for ptr in patterns:
            text = re.sub(ptr, '', text)
        return text

    def remove_punctuations(self, text: str):
        """
        Remove punctuations from the text.

        Parameters
        ----------
        text : str
            The text to be processed.

        Returns
        ----------
        str
            The text with punctuations removed.
        """
        # TODO
        pattern = r'[^\w\s]'
        new_text = re.sub(pattern, '', text)
        return new_text

    def tokenize(self, text: str):
        """
        Tokenize the words in the text.

        Parameters
        ----------
        text : str
            The text to be tokenized.

        Returns
        ----------
        list
            The list of words.
        """
        # TODO
        pattern = r'\b\w+\b'
        list_of_words = re.findall(pattern, text)
        return list_of_words

    def remove_stopwords(self, text: str):
        """
        Remove stopwords from the text.

        Parameters
        ----------
        text : str
            The text to remove stopwords from.

        Returns
        ----------
        list
            The list of words with stopwords removed.
        """
        # TODO
        words = text.split()
        final_words = []

        for word in words:
            lower_word = word.lower()
            if lower_word not in self.stopwords:
                final_words.append(word)
        return final_words

