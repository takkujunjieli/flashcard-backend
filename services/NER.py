import spacy
from keybert import KeyBERT

nlp = spacy.load("en_core_web_sm")  # Use a small NER model
kw_model = KeyBERT()

def extract_keywords(text):
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1,2), stop_words='english')
    return [kw[0] for kw in keywords[:5]]

def extract_entities(section):
    doc = nlp(section)
    entities = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "PERSON", "GPE", "PRODUCT"]]
    return list(set(entities))