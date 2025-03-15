import fitz  # PyMuPDF
import re
import nltk
import spacy
from keybert import KeyBERT
from nltk.tokenize import sent_tokenize

nltk.download('punkt')
nlp = spacy.load("en_core_web_sm")
kw_model = KeyBERT()

def extract_text_with_hierarchy(pdf_path):
    """
    Extracts text while preserving hierarchical structure using font size metadata.
    """
    doc = fitz.open(pdf_path)
    sections = []
    current_section = []
    section_title = "Introduction"  # Default if no heading is detected

    prev_font_size = None
    bullet_pattern = re.compile(r"^(•|-|\d+\.)\s+")  # Detect bullet points

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue  # Skip if no text

            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    font_size = span["size"]

                    if not text:
                        continue

                    # Detect section headings based on font size increase
                    if prev_font_size and font_size > prev_font_size + 1:
                        if current_section:
                            sections.append((section_title, current_section))
                            current_section = []
                        section_title = text  # Treat as new section title
                    prev_font_size = font_size

                    # Preserve bullet points
                    if bullet_pattern.match(text):
                        current_section.append(f"- {text}")  
                    else:
                        current_section.append(text)

    # Append last section
    if current_section:
        sections.append((section_title, current_section))

    return sections


def extract_keywords(text):
    """
    Extracts key phrases from text using KeyBERT.
    """
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1,2), stop_words='english')
    return [kw[0] for kw in keywords[:5]]

def extract_entities(text):
    """
    Extracts named entities (ORG, PERSON, GPE, PRODUCT) using spaCy.
    """
    doc = nlp(text)
    return list(set(ent.text for ent in doc.ents if ent.label_ in ["ORG", "PERSON", "GPE", "PRODUCT"]))

def preprocess_text(pdf_path):
    """
    Extracts structured sections, keywords, and terminology from a PDF file.
    """
    sections = extract_text_with_hierarchy(pdf_path)
    processed_sections = []

    for section_title, content in sections:
        section_text = " ".join(content)  # Combine lines into a paragraph
        keywords = extract_keywords(section_text)
        terminology = extract_entities(section_text)

        processed_sections.append({
            "section_title": section_title,
            "content": content,
            "keywords": keywords,
            "terminology": terminology
        })

    return processed_sections


def extract_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()