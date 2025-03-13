@app.post("/generate_flashcards/")
async def generate_flashcards(file: UploadFile = File(...)):
  file_path = UPLOAD_FOLDER / file.filename
  with file_path.open("wb") as buffer:
    shutil.copyfileobj(file.file, buffer)

  text = extract_text(file_path)
  sections = preprocess_text(text)

  flashcards = []
  for section in sections:
    prompt = format_for_llm(section)
    response = run_llama3_inference(prompt)

    # Split generated response into Q/A (assuming model returns in "Q: ... A: ..." format)
    qa_pairs = response.split("\n")
    for qa in qa_pairs:
      if "Q:" in qa and "A:" in qa:
        question = qa.split("Q:")[1].strip()
        answer = qa.split("A:")[1].strip()
        save_flashcard(section['key_facts'], question, answer, section['terminology'])
        flashcards.append({"question": question, "answer": answer})

  return {"flashcards": flashcards}
