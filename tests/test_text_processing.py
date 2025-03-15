import unittest
from pathlib import Path
from services.text_processing import extract_text_with_hierarchy, extract_keywords, extract_entities, preprocess_text

class TestTextProcessing(unittest.TestCase):

    def setUp(self):
        # Set up the path to the existing PDF file for testing
        self.sample_pdf_path = Path("./MMT.pdf")
        self.sample_text = """
        Introduction
        This is a sample document for testing purposes.
        - Bullet point 1
        - Bullet point 2

        Section 1
        Over the past year or so, much media attention has focused on a new approach to 
        macroeconomics, dubbed Modern Monetary Theory (MMT) by its proponents. MMT burst on 
        the scene in an unusual way. From its name, one might guess that it arose at top universities, as 
        prominent scholars debated the fine points of macroeconomic theory. But that is not the case. 
        Instead, MMT was developed in a small corner of academia and became famous only when some 
        high-profile politicians—particularly Senator Bernie Sanders and Representative Alexandria 
        Ocasio-Cortez—drew attention to it because its tenets conformed to their policy views. 
        """

    def test_extract_text_with_hierarchy(self):
        sections = extract_text_with_hierarchy(self.sample_pdf_path)
        self.assertGreater(len(sections), 0)  # Ensure that sections are extracted
        # Add more specific assertions based on the actual content of MMT.pdf

    def test_extract_keywords(self):
        keywords = extract_keywords(self.sample_text)
        print("Extracted Keywords:", keywords)  # Debug output
        # Adjust the expected keywords based on the actual behavior of KeyBERT
        expected_keywords = ["monetary theory"]
        for keyword in expected_keywords:
            self.assertIn(keyword, keywords)

    def test_extract_entities(self):
        entities = extract_entities(self.sample_text)
        self.assertIn("MMT", entities)

    def test_preprocess_text(self):
        processed_sections = preprocess_text(self.sample_pdf_path)
        self.assertGreater(len(processed_sections), 0)  # Ensure that sections are processed
        # Add more specific assertions based on the actual content of MMT.pdf

if __name__ == "__main__":
    unittest.main()