import json
import subprocess
import os
from pathlib import Path
from core.database import save_flashcard

GENIE_PATH = "/path/to/genie"
MODEL_PATH = "/path/to/llama3.qnn"

PROCESSED_FOLDER = Path("./processed")  # Path where structured JSON is stored


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


def cleanup_json_file(filename):
    """
    Deletes the processed JSON file after flashcards have been generated successfully.
    """
    processed_file_path = PROCESSED_FOLDER / f"{filename}.json"

    if processed_file_path.exists():
        try:
            os.remove(processed_file_path)
            print(f"Deleted old JSON file: {processed_file_path}")
        except Exception as e:
            print(f"Error deleting JSON file: {processed_file_path} - {str(e)}")


def efficient_flashcard_generation(filename):
    """
    Generates flashcards using pre-extracted structured text.
    Implements a fallback mechanism to prevent JSON deletion if generation fails.
    """
    processed_file_path = PROCESSED_FOLDER / f"{filename}.json"

    if not processed_file_path.exists():
        return {"error": "Processed file not found. Please upload again."}

    try:
        # Read structured data instead of re-extracting
        with open(processed_file_path, "r", encoding="utf-8") as f:
            structured_text = json.load(f)

        flashcards = []
        for section in structured_text:
            prompt = f"""
            You are an AI assistant that generates flashcards from uploaded documents. Your task is to extract key concepts, summarize them into questions and answers, and present them as flashcards. 

            ### Instructions:
            1. **Extract 10 key concepts** from the document. Choose concepts that are important, fundamental, or commonly tested.
            2. **Generate a question and an answer** for each concept:
            - The **question** should be concise but meaningful (max **100 words**).
            - The **answer** should be informative and accurate (max **100 words**).
            - Both should be clear, direct, and focused on learning.
            3. **Avoid vague or overly general questions**. Ensure the questions test understanding rather than just recalling definitions.
            4. **Maintain a structured output format** for easy processing.

            ### **Output Format (JSON)**
            ```json
            {
            "flashcards": [
                {
                "question": "What is [concept] and why is it important?",
                "answer": "[Concise explanation of concept within 100 words.]"
                },
                {
                "question": "How does [concept] work in [context]?",
                "answer": "[Detailed yet concise answer within 100 words.]"
                },
                ...
            ]
            }
            """

            response = run_llama3_inference(prompt)

            if "Error" in response or "Genie inference failed" in response:
                raise RuntimeError(f"Inference failed: {response}")

            # Parse and store flashcards
            qa_pairs = response.split("\n")
            for qa in qa_pairs:
                if "Q:" in qa and "A:" in qa:
                    question = qa.split("Q:")[1].strip()
                    answer = qa.split("A:")[1].strip()
                    keywords = section.get("keywords", [])
                    terminology = section.get("terminology", [])

                    save_flashcard(question, answer, terminology, keywords)

                    flashcards.append(
                        {
                            "question": question,
                            "answer": answer,
                            "terminology": terminology,
                            "keywords": keywords,
                        }
                    )

        # If everything was successful, delete the JSON file
        cleanup_json_file(filename)

        return flashcards

    except Exception as e:
        print(f"Error generating flashcards: {str(e)}")
        return {"error": f"Flashcard generation failed: {str(e)}"}
