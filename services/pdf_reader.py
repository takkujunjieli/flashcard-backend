import re
import pdfminer
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTTextLineHorizontal

def extract_text_with_hierarchy(pdf_path):
    sections = []
    current_section = []
    prev_font_size = None
    section_title = None
    bullet_pattern = re.compile(r"^(•|-|\d+\.)\s+")  # Bullet points and numbered lists

    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, (LTTextBoxHorizontal, LTTextLineHorizontal)):
                text = element.get_text().strip()
                font_size = getattr(element, 'size', None)  # Try to get font size
                
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

def format_sections_for_llm(sections):
    """
    Formats sections into structured text suitable for an LLM.
    """
    formatted_text = []
    for title, content in sections:
        formatted_text.append(f"## {title}\n\n" if title else "")
        formatted_text.extend(content)
        formatted_text.append("\n")  # Add spacing between sections
    
    return "\n".join(formatted_text)

# Usage:
pdf_path = "../MMT.pdf"
structured_sections = extract_text_with_hierarchy(pdf_path)
final_text = format_sections_for_llm(structured_sections)

print(final_text)  # Ready for feeding into Llama 3
