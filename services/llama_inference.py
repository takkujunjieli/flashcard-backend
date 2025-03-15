import subprocess
import json
from services.text_processing import preprocess_text
from core.database import save_flashcard

GENIE_PATH = "/path/to/genie"  # Update with actual Genie executable path
MODEL_PATH = "/path/to/llama3.qnn"  # Update with actual compiled QNN model

def run_llama3_inference(prompt):
    """
    Runs on-device inference using Genie and the compiled QNN model.
    """
    command = [GENIE_PATH, "--model", MODEL_PATH, "--input", prompt]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = json.loads(result.stdout)
        return output.get("generated_text", "")
    except json.JSONDecodeError:
        return "Error in inference output."
    except subprocess.CalledProcessError as e:
        return f"Genie inference failed: {e.stderr}"
    


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
        You are a professional lecturer. Your task is to help students memorize the content by generating Q&A pairs.
        Each Q&A pair should address one keyword from the content. Ensure that both the question and answer are concise,
        with a word limit of less than 30 words each.

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