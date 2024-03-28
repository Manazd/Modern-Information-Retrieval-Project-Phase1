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
        with open('stopwords.txt', 'r') as file:
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
        
        # Apply stemming
        stemmer = PorterStemmer()
        normalized_text = ' '.join(stemmer.stem(word) for word in lower_text.split())

        # # Apply lemmatization
        # tokenized = word_tokenize(lower_text)
        # lemmatizer = WordNetLemmatizer()
        # normalized_text = ' '.join(lemmatizer.lemmatize(token) for token in tokenized)

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
        return

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
        return

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
        return

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
        return

