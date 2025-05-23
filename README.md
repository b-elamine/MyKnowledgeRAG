# My Knowledge RAG

A Retrieval-Augmented Generation (RAG) chatbot powered by OpenAI embeddings to answer questions using your personal knowledge base: CV, master thesis, GitHub repos, and research papers.

---

## 🔍 Overview

This project builds a personalized chatbot that leverages your **own data** to answer questions. It uses OpenAI embeddings and FAISS to enable fast and accurate document search and retrieval.

**Sources supported:**
- 📄 PDFs (CVs, theses, research papers)
- 💻 GitHub repositories (code)
- 🧠 Chunked embeddings with metadata stored locally

---

## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/b-elamine/MyKnowledgeRAG
cd MyKnowledgeRAG
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Configuration

You must create a `.env` file in the project root with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key
GITHUB_USERNAME=your_github_username
GITHUB_TOKEN=your_github_personal_access_token
```

- `OPENAI_API_KEY`: Required to generate embeddings.
- `GITHUB_USERNAME` and `GITHUB_TOKEN`: Used to authenticate and clone your GitHub repositories automatically.

> 💡 Tip: You can generate a GitHub token at https://github.com/settings/tokens (give it `repo` access if you're cloning private repos).

---

## 🗂️ Data Preparation

### 1. PDFs

Put all relevant documents inside the folder:

```
data/pdfs/
```

Examples:
- Your updated CV
- Academic thesis or dissertation
- Research papers you've written or use

Accepted formats: `.pdf`

### 2. GitHub Projects

Your repositories will be cloned automatically using the GitHub token. You’ll specify the repo URLs or names inside the script or configuration.

They will be stored in:

```
data/github_projects/
```

> ⚠️ This folder is **ignored by Git** to prevent uploading private code.

---

## 🚀 Usage

### Step 1: Extract & Process Data

```bash
python src/data_processing.py
```

- Loads PDFs and GitHub files
- Extracts and preprocesses text
- Chunks the content into smaller units
- Saves the output to `raw_data.pkl`

---

### Step 2: Create and Save Embeddings

```bash
python src/embedding.py
```

- Loads chunks
- Uses OpenAI Embeddings API
- Batches embedding requests to avoid token limits
- Saves `embeddings.pkl` with chunks and vectors

---

### Step 3: Build Vector Store

```bash
python src/vector_store.py
```

- Loads `embeddings.pkl`
- Creates FAISS index
- Saves index and metadata locally

---

### Step 4: Query Your Knowledge Base

Example usage in `test.py`:

```bash
python src/test.py
```

You can change the query in the script like this:

```python
query = "What are the main contributions of the thesis?"
```

It will:
- Embed the question
- Search FAISS for most similar document chunks
- Return top matches

---

## 📁 Folder Structure

```
PersonalRAGBot/
├── data/
│   ├── pdfs/                 # Your documents (CV, thesis, papers)
│   ├── github_projects/      # Auto-cloned repos (gitignored)
│   └── vector_store/         # FAISS index + chunk metadata
├── src/                      # All core logic scripts
│   ├── data_processing.py
│   ├── embedding.py
│   ├── vector_store.py
│   └── test.py
├── .env                      # Secrets (NOT tracked by Git)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🛡️ Notes on Cost & Privacy

- **Costs:** Embeddings API is not free; use batching and caching to reduce calls.
- **Privacy:** Everything (documents, GitHub code, embeddings) is stored and processed locally except for the embedding API calls.

---

## 📌 To Do

- Add LLM-based answer generation using retrieved chunks
- Optional web-based chatbot interface
- More advanced PDF structure handling

---


