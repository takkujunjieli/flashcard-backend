# Flashcard Generator - Backend

## Description

The Flashcard Generator is an AI-powered application that allows users to generate flashcards from uploaded PDF files. The app processes structured text, extracts keywords and entities, and generates relevant question-answer pairs to aid learning. This project is designed to run locally without cloud dependency and is integrated with Qualcomm technologies for optimized on-device inference.

## Developers & Contact

- **[Junjie Li]** - alvinbluy@gmail.com
- **[Hui Zhou]** - zhouhui2023cs@gmail.com
- **[Meredith Luo]** - meredithluo710@gmail.com
- **[Rouming Zhang]** - lotus20210417@gmail.com
- **[Tiantian Huang]** - huangtiantian0430@gmail.com


## Backend and Frontend Link

- Backend: https://github.com/takkujunjieli/flashcard-backend main branch
- Frontend: https://github.com/mereluo/flashcard-generator main branch

## Setup Instructions

Prerequisites

Ensure you have the following dependencies installed:

```
Python 3.8+
Node.js (>= 14.0.0)
npm (>= 6.0.0)
```

## Backend Installation

Clone the repository:

```
git clone https://github.com/your-repo/flashcard-backend.git
cd flashcard-backend
```

Create a virtual environment:

```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install dependencies:

```
pip install -r requirements.txt
```

Download necessary NLP models:

```
python -m nltk.downloader punkt
python -m spacy download en_core_web_sm
```


Start the FastAPI server:
```

uvicorn main:app --reload
```

The API will be available at http://127.0.0.1:8000

## Usage

1. Upload a PDF to generate flashcards automatically.
2. Choose the selected type of card number, role and purpose, or customize your flashcard generation prompt.
3. Edit flashcards using the interactive editor.
4. Navigate through flashcards using the carousel or list view.

## License
This project is licensed under the MIT License.

```
MIT License

Copyright (c) [2025] [NextLv Team]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
