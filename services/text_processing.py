import re
import nltk
import spacy
from keybert import KeyBERT
from nltk.tokenize import sent_tokenize

nltk.download('punkt')
nlp = spacy.load("en_core_web_sm")
kw_model = KeyBERT()

def extract_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_text_with_hierarchy(text):
    sections = []
    current_section = []
    prev_font_size = None
    section_title = None
    bullet_pattern = re.compile(r"^(•|-|\d+\.)\s+")  # Bullet points and numbered lists

    lines = text.split('\n')
    for line in lines:
        text = line.strip()
        font_size = None  # Placeholder for font size logic if needed
        
        if font_size is not None:
            if prev_font_size and font_size > prev_font_size:
                # New section detected (bigger font means heading)
                if current_section:
                    sections.append((section_title, current_section))
                    current_section = []
                section_title = text
            prev_font_size = font_size
        
        if bullet_pattern.match(text):
            current_section.append(f"- {text}")  # Normalize bullet format
        else:
            current_section.append(text)

    if current_section:
        sections.append((section_title, current_section))

    return sections

def extract_keywords(text):
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1,2), stop_words='english')
    return [kw[0] for kw in keywords[:5]]

def extract_entities(section):
    doc = nlp(section)
    entities = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "PERSON", "GPE", "PRODUCT"]]
    return list(set(entities))

def preprocess_text(text):
    sections = extract_text_with_hierarchy(text)
    processed_sections = []
    for section in sections:
        key_facts = " ".join(section[:5])  # First few sentences
        terminology = extract_entities(" ".join(section))
        processed_sections.append({
            "key_facts": key_facts,
            "terminology": terminology
        })
    return processed_sections
