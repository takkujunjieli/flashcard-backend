import re
from PyPDF2 import PdfReader
from pathlib import Path
from keybert import KeyBERT
import spacy

PROCESSED_FOLDER = Path("./processed")

# Initialize KeyBERT model
kw_model = KeyBERT()

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_text_with_pypdf2(pdf_path):
    """
    Extracts text while preserving hierarchical structure using PyPDF2.
    """
    sections = []
    current_section = []
    section_title = "Introduction"  # Default if no heading is detected

    bullet_pattern = re.compile(r"^(•|-|\d+\.)\s+")  # Detect bullet points

    reader = PdfReader(pdf_path)
    for page in reader.pages:
        text = page.extract_text()

        if not text:
            continue

        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Detect section headings based on simple heuristics (e.g., all caps)
            if line.isupper():
                if current_section:
                    sections.append((section_title, current_section))
                    current_section = []
                section_title = line  # Treat as new section title
            else:
                # Preserve bullet points
                if bullet_pattern.match(line):
                    current_section.append(f"- {line}")
                else:
                    current_section.append(line)

    # Append last section
    if current_section:
        sections.append((section_title, current_section))

    return sections

def preprocess_text(pdf_path):
    """
    Extracts structured sections, keywords, and terminology from a PDF file using PyPDF2.
    """
    try:
        structured_data = extract_text_with_pypdf2(pdf_path)
        processed_sections = []

        for section in structured_data:
            section_title = section[0]
            content = section[1]
            keywords = extract_keywords(" ".join(content))
            terminology = extract_entities(" ".join(content))

            processed_sections.append({
                "section_title": section_title,
                "content": content,
                "keywords": keywords,
                "terminology": terminology
            })

        print(f"Processed sections: {processed_sections}")

        return processed_sections
    except Exception as e:
        print(f"Error processing text: {e}")
        raise

def extract_keywords(text):
    """
    Extracts key phrases from text using KeyBERT.
    """
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english')
    return [kw[0] for kw in keywords[:5]]

def extract_entities(text):
    """
    Extracts named entities (ORG, PERSON, GPE, PRODUCT) using spaCy.
    """
    doc = nlp(text)
    return list(set(ent.text for ent in doc.ents if ent.label_ in ["ORG", "PERSON", "GPE", "PRODUCT"]))

def extract_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()