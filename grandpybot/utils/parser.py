from nltk.tokenize import sent_tokenize, word_tokenize

from .stopwords import STOP_WORDS


class Parser:
    """
        This class provide functionalities to tokenize text and filter
        sentences to extract the keywords.
    """

    def __init__(self):
        pass

    def raw_to_sentences(self, raw_text):
        ''' Returns a raw text as a list of sentences '''
        sentences = []
        temp_sentences = sent_tokenize(raw_text)
        for s in temp_sentences:
            for ss in s.split(","):
                sentences.append(ss.strip())
        return sentences

    def get_keywords(self, sentence):
        ''' Returns the keywords of a sentence '''
        return self._words_filter(self._tokenize(sentence))

    def _tokenize(self, sentence):
        '''Tokenize the sentence and return list of words'''
        if sentence is None:
            return None
        sentence = "".join(c if c not in "'-" else " " for c in sentence)
        words = word_tokenize(sentence, language='french')
        return words

    def _words_filter(self, words):
        '''filter a list of words by removing stop words'''
        if words is None:
            return None
        words_filtered = []
        for w in words:
            if w.lower() not in STOP_WORDS:
                words_filtered.append(w)
        return words_filtered
