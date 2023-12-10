import spacy
from spacy.matcher import Matcher

# Load the language model
nlp = spacy.load('en_core_web_sm')

# Initialize the matcher with the shared vocab
matcher = Matcher(nlp.vocab)
