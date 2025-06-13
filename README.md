# Traffic Rules Assistant (Tamil Nadu RAG Chatbot)

An AI-powered assistant built using Retrieval-Augmented Generation (RAG) that provides context-aware answers about Tamil Nadu traffic rules, penalties, and driver rights. It combines semantic search with LLMs for accurate, explainable, and trustworthy responses.

---
![Alt text](https://github.com/madhans476/repo-image/blob/main/traffic_rules_assistant/Screenshot%202025-06-13%20163336.png)
![Alt text](https://github.com/madhans476/repo-image/blob/main/traffic_rules_assistant/Screenshot%202025-06-13%20163402.png)
## Overview

This project extracts legal content from a government-issued traffic PDF and makes it queryable via natural language questions using a custom-built RAG pipeline. It uses:

* `sentence-transformers` for generating document embeddings
* `FAISS` for fast semantic retrieval
* `LangChain` with `Groq` LLM backend for fast and accurate response generation
* `FastAPI` to expose the system as an API

The assistant is designed to provide concise, legally grounded, and verifiable answers.

---

## Target Audience

* Citizens of Tamil Nadu
* Driving school instructors and trainees
* Traffic law educators
* Law enforcement agencies
* AI/ML enthusiasts learning about RAG pipelines

---

## Prerequisites

* Python 3.11+
* Basic terminal/CLI knowledge
* Internet access for LLM API (Groq)
* Groq API key (free tier available)

---

## Installation

```bash
# Clone the repository
https://github.com/madhans476/traffic_rules_assistant.git

cd traffic_rules_assistant

# Create environment
uv venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
uv pip install -r requirements.txt
```

---

## Environment Setup

### `.env` file (create at root):

```
GROQ_API_KEY=your-groq-api-key-here
```

### Required files:

* `data/TN Traffic rules.pdf`

---

## Usage

### 1. Text Extraction

```bash
python src/text_extraction.py
```

### 2. Chunking

```bash
python src/chunking.py
```

### 3. Embedding + FAISS Index Creation

```bash
python src/embedding.py
```

### 4. CLI Chatbot

```bash
python src/main.py
```

### 5. API (FastAPI)

```bash
uvicorn api.app:app --reload
# Visit http://localhost:8000/docs
```

---

## Data Requirements

* Input: A traffic rulebook in `.pdf`
* Output:

  * `.txt` file with full extracted text
  * `.json` with clean overlapping chunks
  * `.idx` FAISS index file

---

## Testing

Manual test cases:

* Ask questions from the CLI or Swagger UI
* Evaluate LLM responses vs. original PDF

(Automated tests can be added using `pytest`.)

---

## Configuration

### Chunking:

* `chunk_size = 300`
* `overlap = 50`

### FAISS:

* `IndexFlatIP` used for vector similarity search

### LLM (Groq):

* Model: `mixtral-8x7b-32768` (default)
* Temperature: `0.3`

---

## Methodology

1. Parse legal traffic PDF to text
2. Split text into semantic chunks
3. Embed chunks using `sentence-transformers`
4. Store in `FAISS` for fast vector search
5. On query:

   * Embed the question
   * Retrieve top-k relevant chunks
   * Pass to Groq LLM using LangChain
6. Return clean, structured answer

---

## Performance

* Fast local retrieval (\~50–100 ms)
* Groq LLM response: \~100 tokens/ms
* Accurate context-based answers
* No hallucinations (guardrails in prompt)

---

## License

MIT License. See `LICENSE` file.

---

## Contributing

Pull requests welcome!

* Fork the repo
* Create a new branch
* Submit a pull request with a meaningful message

---

## Changelog

### v1.0.0 (June 2025)

* Initial public release
* Added full pipeline: Extraction, Chunking, Embedding, Retrieval, Generation
* FastAPI API + CLI support
* Groq + LangChain integration

---

## Citation

If you use this in academic work:

```
@misc{trafficassistant2025,
  title={Tamil Nadu Traffic Rules Assistant using RAG},
  author={Madhan S},
  year={2025},
  howpublished={\url{https://github.com/madhans476/traffic_rules_assistant}}
}
```

---

## Contact

**Maintainer:** Madhan S
**Email:** [mail](mailto:22bds036@iiitdwd.ac.in)
**GitHub:** [@madhans476](https://github.com/madhans476)
