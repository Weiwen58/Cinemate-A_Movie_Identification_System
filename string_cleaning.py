import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


def remove_stopwords(text_list):
    # Get the list of English stop words
    stop_words = set(stopwords.words('english')) #set to be faster to search
    # Remove stop words from the list of words
    filtered_words = [word for word in text_list if word not in stop_words]
    return filtered_words


def remove_punctuation(input_string):
    translator = str.maketrans("", "", string.punctuation)
    return input_string.translate(translator)


def verb_stemming(text_list):
    # Initialize the Porter Stemmer
    porter = PorterStemmer()
    # Perform stemming on each word
    stemmed_words = [porter.stem(word) for word in text_list]
    return stemmed_words


def clean_string_ret_string(input): #returns a string
    clean_input = input.lower()
    clean_input = remove_punctuation(clean_input)
    
    clean_input_list = word_tokenize(clean_input)# tokenized the lowercase, non-punctuated string to avoid redundant tokenizing and joining.
    
    clean_input_list = remove_stopwords(clean_input_list)
    clean_input_list = verb_stemming(clean_input_list)
    
    return ' '.join(clean_input_list)
    

def clean_string_ret_list(input):# returns a list
    clean_input = input.lower()
    clean_input = remove_punctuation(clean_input)
    
    clean_input_list = word_tokenize(clean_input)# tokenized the lowercase, non-punctuated string to avoid redundant tokenizing and joining.
    
    clean_input_list = remove_stopwords(clean_input_list)
    clean_input_list = verb_stemming(clean_input_list)
    
    return clean_input_list
    