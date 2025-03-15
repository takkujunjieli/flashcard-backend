import sys
import os

# Add the root directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from services.llm_inference import run_llama3_inference

def test_run_llama3_inference():
    sample_prompt = "Explain the theory of relativity in simple terms."
    result = run_llama3_inference(sample_prompt)
    print("Inference Result:", result)

if __name__ == "__main__":
    test_run_llama3_inference()