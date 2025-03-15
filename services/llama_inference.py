import subprocess
import json

from services.text_processing import preprocess_text
from core.database import save_flashcard  # Import the save_flashcard function

def run_llama3_inference(prompt):
    command = f"./genie --model llama3.qnn --input '{prompt}'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    try:
        output = json.loads(result.stdout)
        return output.get("generated_text", "")
    except json.JSONDecodeError:
        return "Error in inference output."

def efficient_flashcard_generation(pdf_path):
    """
    Generates flashcards efficiently by structuring input before sending to Llama 3.
    """
    # Step 1: Preprocess text (extract structured content)
    structured_text = preprocess_text(pdf_path)

    flashcards = []
    for section in structured_text:
        # Step 2: Format optimized prompt for Llama 3
        prompt = f"""
        Section: {section['section_title']}
        Content: {', '.join(section['content'])}
        
        Generate 3 question-answer pairs relevant to the content.
        """

        # Step 3: Run inference with structured prompt
        response = run_llama3_inference(prompt)

        # Step 4: Parse generated flashcards
        qa_pairs = response.split("\n")
        for qa in qa_pairs:
            if "Q:" in qa and "A:" in qa:
                question = qa.split("Q:")[1].strip()
                answer = qa.split("A:")[1].strip()
                keywords = section.get('keywords', [])
                terminology = section.get('terminology', [])
                
                # Save flashcard to the database
                save_flashcard(question, answer, terminology, keywords)
                
                flashcards.append({
                    "question": question,
                    "answer": answer,
                    "terminology": terminology,
                    "keywords": keywords
                })

    return flashcards