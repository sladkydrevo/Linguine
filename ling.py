import spacy
import spacy_udpipe
import pandas as pd
import re
import chardet
import json
import os

from collections import Counter

def analyze_text(text):
    """Returns a dictionary with various metrics from the analyzed text."""
    text_data = {
        "text" : text,
        "tokens_data" : text.get_tokens_data(), 
        "longest" : text.get_longest(), 
        "most_frequent" : text.get_frequency_list(), 
        "sentence_lengths" : text.get_sentence_lengths(), 
        "word_lengths" : text.get_word_lengths()
    }
    return text_data

def read_decode_file(file, decoded=None):
    """Reads and decodes file content based on its encoding."""
    loaded_text = file.read()
    encoding_type = chardet.detect(loaded_text)
    if encoding_type["encoding"] == "utf-8":
        decoded = loaded_text.decode("utf-8")
    elif encoding_type["encoding"] == "ascii":
        decoded = loaded_text.decode("ascii")
    return decoded

def load_json(json_file, app):
    """Loads and returns JSON data from a file."""
    path = os.path.join(app.static_folder, "data", json_file)
    with open(path) as f:
        data = json.load(f)
    return data
    
def get_pos_list(pos, doc):
    """Returns list of lemmas of words matching a given part of speech."""
    return [word.lemma_ for word in doc if word.pos_ == pos]

def get_most_frequent(pos):
    """Returns the most frequent item in a list."""
    return Counter(pos).most_common(1)

class AnalyzedText:
    """ 
    A class for analyzing and processing text data in either Czech or English, leveraging spaCy models.

    Attributes:
    -----------
    text : str
        The input text to be analyzed.
    language : str
        The language of the input text, either "cs" for Czech or any other string for English.
    doc : spaCy Doc
        The processed document object created using the appropriate spaCy model.
    characters_count : int
        The number of characters in the input text.
    tokens : list of spaCy Tokens
        A list of tokens from the text, excluding punctuation, digits, and spaces.
    tokens_count : int
        The number of tokens in the text after filtering.
    sentences : list of spaCy Sentences
        A list of sentences in the text.
    sentence_count : int
        The number of sentences in the text.
    types : list of str
        A list of lemmatized tokens from the text.
    types_count : int
        The number of unique types (lemmas) in the text.
    ttr : float
        The type-token ratio, which is the ratio of unique types to the total number of tokens.

    Methods:
    --------
    __str__():
        Returns the original text as a string representation of the object.

    get_frequency_list():
        Returns a dictionary with the most frequent noun, adjective, and verb in the text, along with their frequencies.

    get_longest():
        Returns a list of the longest words in the text.

    get_tokens_data(df=False):
        Returns a list of dictionaries, each containing detailed information about tokens in the text.
        If df=True, returns a pandas DataFrame instead.

    get_sentence_lengths():
        Returns a list of sentence lengths (number of tokens per sentence).
        Also calculates and stores the average sentence length.

    get_word_lengths():
        Returns a list of word lengths (number of characters per word).
        Also calculates and stores the average word length.

    regex_explore(regex):
        Returns a list of sentences that match a given regular expression or word.
        Each sentence is highlighted as so the matching parts of the sentence are bold and with 
        underline in the rendered template.
        Each sentence is also classified as declarative, interrogative, or exclamatory.
    """

    def __init__(self, text, language):
        self.text = text
        self.language = language
        
        if self.language == "cs":
            nlp = spacy_udpipe.load("cs")
        else:
            nlp = spacy.load("en_core_web_sm")
            
        self.doc = nlp(text)
        
        self.characters_count = len(text)
        self.tokens = [token for token in self.doc if not token.is_punct and not token.is_digit and not token.is_space]
        self.tokens_count = len(self.tokens)
        self.sentences = [sentence for sentence in self.doc.sents] 
        self.sentence_count = len(self.sentences)
        self.types = [token.lemma_ for token in self.tokens]
        self.types_count = len(set(self.types))
        self.ttr = self.types_count / self.tokens_count
        
    def __str__(self):
        return self.text

    def get_frequency_list(self):
        doc = self.doc

        freq_nouns = get_most_frequent(get_pos_list("NOUN", doc))
        freq_adjs = get_most_frequent(get_pos_list("ADJ", doc))
        freq_verbs = get_most_frequent(get_pos_list("VERB", doc))

        frequencies = {
            "noun" : freq_nouns[0] if len(freq_nouns) > 0 else (None, 0), 
            "adjective" : freq_adjs[0] if len(freq_adjs) > 0 else (None, 0), 
            "verb" : freq_verbs[0] if len(freq_verbs) > 0 else (None, 0)
        }
        
        return frequencies
    
    def get_longest(self):
        tokens = self.tokens
        longest = ""
        for word in tokens:
            if len(word) > len(longest):
                longest = word
        longest_words = [str(word) for word in tokens if len(word) == len(longest)]
        longest_words = list(set(longest_words))
        return longest_words

    def get_tokens_data(self, df=False):
        doc = self.doc
        text_data = []
        for token in doc:
            if not token.is_punct and not token.is_digit and not token.is_space:
                token_info = {
                    "token" : token.text, 
                    "lemma" : token.lemma_, 
                    "pos" : token.pos_, 
                    "deprel" : token.dep_, 
                    "stopword" : token.is_stop
                }
            
                text_data.append(token_info)
            
        if df:
            text_data = pd.DataFrame(text_data)
            
        return text_data
    
    def get_sentence_lengths(self):
        sentence_lengths = []
        for sentence in self.sentences:
            count = 0
            for token in sentence:
                if not token.is_punct and not token.is_digit and not token.is_space:
                    count += 1
            sentence_lengths.append(count)
            
        self.avg_sent_length = sum(sentence_lengths) / len(sentence_lengths)
        
        return sentence_lengths
    
    def get_word_lengths(self):
        word_lengths = [len(token) for token in self.tokens]
        self.avg_word_length = sum(word_lengths) / len(word_lengths)
        return word_lengths
    
    def regex_explore(self, regex):
        doc = self.doc
        
        pattern = re.compile(regex)
        
        matching_sentences = []
        for sentence in list(doc.sents):
            if pattern.findall(sentence.text):
                sentence_type = (
                    "Interrogative" if sentence.text.endswith("?") else
                    "Exclamatory" if sentence.text.endswith("!") else
                    "Declarative"
                )
                
                highlihted_sentence = pattern.sub(lambda match: f"<b><u>{match.group(0)}</u></b>", sentence.text)
                
                sentence_info = {
                    "sentence" : highlihted_sentence,
                    "length" : len([token.text for token in sentence if not token.is_punct and not token.is_space]),
                    "type" : sentence_type
                }
                matching_sentences.append(sentence_info)
            
        return matching_sentences