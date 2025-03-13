def generate_flashcard_prompt(section_title, key_facts, terminology):
    """
    Generates a structured prompt to pass to the LLM for flashcard generation.
    """
    prompt = f"""
    You are an AI assistant that generates educational flashcards.

    ### Input Text Section:
    **Title:** {section_title}
    **Key Facts:** 
    {key_facts}

    ### Important Terminology:
    {', '.join(terminology)}

    ### Instructions:
    1. Generate **three question-answer flashcards** based on the text.
    2. Ensure that each **answer contains at least one of the terminology words**.
    3. Mark the terminology words in the answers using **double brackets**, e.g., `[[Neural Networks]]`.
    4. Provide **a short definition for each terminology word** in a separate section.

    ### Expected Output Format:
    - **Flashcards (Q&A):**
      - **Q1:** [Generated question]
      - **A1:** [Generated answer with `[[highlighted]]` terminology]
      - **Q2:** [Generated question]
      - **A2:** [Generated answer with `[[highlighted]]` terminology]
      - **Q3:** [Generated question]
      - **A3:** [Generated answer with `[[highlighted]]` terminology]

    - **Terminology Flashcards:**
      - **Neural Networks** → A computational model inspired by the human brain, consisting of layers of interconnected nodes.
      - **Backpropagation** → An algorithm used to train neural networks by adjusting weights based on error minimization.
      - **Tensor** → A multi-dimensional array used in machine learning and deep learning computations.

    Generate the flashcards based on the given text section.
    """
    return prompt


def generate_definition_prompt(term, context):
    """
    Generates a prompt for LLM to provide a context-aware definition of a term.
    """
    prompt = f"""
    You are an AI assistant generating precise, context-aware definitions.
    
    ### Term:
    "{term}"

    ### Context:
    "{context}"

    ### Instructions:
    1. Provide a **concise definition** of the term in the context provided.
    2. Keep the explanation **simple and easy to understand**.
    3. Ensure the definition is **specific to the given context** and not a generic definition.
    4. Output in the following format:
    
       - **{term}** → [Definition]
    """
    return prompt
