import json
import requests
from pathlib import Path
import yaml
import os
# from core.database import save_flashcard

# Load configuration
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

API_KEY = config["api_key"]
MODEL_SERVER_BASE_URL = config["model_server_base_url"]
SLUG = config["workspace_slug"]

PROCESSED_FOLDER = Path("./processed")  # Path where structured JSON is stored


def run_llama3_inference(prompt):
    """
    Runs inference using the AnythingLLM API.
    """
    url = f"{MODEL_SERVER_BASE_URL}/workspace/{SLUG}/chat"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + API_KEY
    }
    payload = {
        "message": prompt,
        "mode": "chat",
        "sessionId": "flashcard-session",
        "attachments": [],
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        output = response.json()
        return output.get("textResponse", "")
    except requests.exceptions.RequestException as e:
        return f"AnythingLLM API request failed: {str(e)}"
    except json.JSONDecodeError:
        return "Error in inference output."


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
            print(
                f"Error deleting JSON file: {processed_file_path} - {str(e)}")


def generate_base_prompt(userPrompt):
    """
    Adjusts the first sentence of the prompt based on keyword conditions.
    """
    lower_prompt = userPrompt.lower()

    if "students" in lower_prompt:
        if "review" in lower_prompt:
            return "You are a professional lecturer. Your task is to help the student (user) memorize the content by generating Q&A pairs."
        if "interview" in lower_prompt:
            return "Your task is to help students interview by generating Q&A pairs."

    if "interviewee" in lower_prompt:
        if "interview" in lower_prompt:
            return "Your task is to help interviewees interview using Q&A pairs."
        if "review" in lower_prompt:
            return "Your task is to help interviewees memorize the content using Q&A pairs."

    return "You are a professional lecturer. Your task is to help memorize the content by generating Q&A pairs."


def efficient_flashcard_generation(filename, userPrompt):
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

        first_sentence = generate_base_prompt(userPrompt)

        flashcards = []
        for section in structured_text:
            prompt = f"""
            {first_sentence}
            Section: {section['section_title']}
            Content: {', '.join(section['content'])}
            keywords: {section.get('keywords', [])}
            terminology: {section.get('terminology', [])}


            Each Q&A pair should address one keyword from the content. Ensure that both the question and answer are concise,
            with a word limit of less than 30 words each.

            {userPrompt}
            """

            response = run_llama3_inference(prompt)
            print(f"response: {response}")

            if "Error" in response or "Genie inference failed" in response:
                raise RuntimeError(f"Inference failed: {response}")

            # Parse and store flashcards
            qa_pairs = response.split("\n")

            flashcards = []
            question = None  # Temporary storage for the current question

            for line in qa_pairs:
                line = line.strip()
                if line.startswith("Q:"):
                    question = line[2:].strip()  # Extract the question text
                elif line.startswith("A:") and question:
                    answer = line[2:].strip()  # Extract the answer text
                    keywords = section.get('keywords', [])
                    terminology = section.get('terminology', [])

                    flashcards.append({
                        "question": question,
                        "answer": answer,
                        "terminology": terminology,
                        "keywords": keywords
                    })

                    question = None  # Reset for the next Q&A pair
            # Print the generated flashcards for debugging
            print("Generated flashcards:", flashcards)

            # If everything was successful, delete the JSON file
            cleanup_json_file(filename)

            return flashcards

    except Exception as e:
        print(f"Error generating flashcards: {str(e)}")
        return {"error": f"Flashcard generation failed: {str(e)}"}

def efficient_definition_generation(filename, terminology):
    """
    Generates definitions and extensions for the given terminology using pre-extracted structured text.
    Implements a fallback mechanism to prevent JSON deletion if generation fails.
    """
    processed_file_path = PROCESSED_FOLDER / f"{filename}.json"

    if not processed_file_path.exists():
        return {"error": "Processed file not found. Please upload again."}

    try:
        # Read structured data instead of re-extracting
        with open(processed_file_path, "r", encoding="utf-8") as f:
            structured_text = json.load(f)

        definitions = []
        prompt = f"""
        You are a professional lecturer. Your task is to provide a clear and concise definition and extension for the following term:
        Term: {terminology}

        Definition:
        Extension:
        """

        response = run_llama3_inference(prompt)
        print(f"response: {response}")

        if "Error" in response or "Genie inference failed" in response:
            raise RuntimeError(f"Inference failed: {response}")

        # Parse and store definitions and extensions
        lines = response.split("\n")
        definition = None
        extension = None

        for line in lines:
            line = line.strip()
            if line.startswith("Definition:"):
                definition = line[len("Definition:"):].strip()
            elif line.startswith("Extension:"):
                extension = line[len("Extension:"):].strip()

        if definition and extension:
            definitions.append({
                "term": terminology,
                "definition": definition,
                "extension": extension
            })

        # Print the generated definitions for debugging
        print("Generated definitions:", definitions)

        # If everything was successful, delete the JSON file
        cleanup_json_file(filename)

        return definitions

    except Exception as e:
        print(f"Error generating definitions: {str(e)}")
        return {"error": f"Definition generation failed: {str(e)}"}