def run_llama3_inference(prompt):
  # Call the Genie tool to run inference
  command = f"./genie --model llama3.qnn --input '{prompt}'"
  result = subprocess.run(command, shell=True, capture_output=True, text=True)

  try:
    output = json.loads(result.stdout)
    return output.get("generated_text", "")
  except json.JSONDecodeError:
    return "Error in inference output."