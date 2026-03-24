# 🏠 Real Estate Research Tool

A RAG (Retrieval-Augmented Generation) powered research assistant that lets you scrape real estate listing URLs, store them in a vector database, and ask natural language questions about the content.

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| LLM | Groq (`llama-3.3-70b-versatile`) |
| Embeddings | HuggingFace (`sentence-transformers/all-mpnet-base-v2`) |
| Vector Store | ChromaDB |
| Document Loader | LangChain `UnstructuredURLLoader` |
| Text Splitter | LangChain `RecursiveCharacterTextSplitter` |
| QA Chain | LangChain `RetrievalQAWithSourcesChain` |

---

## 📁 Project Structure

```
real-estate-project/
│
├── rag.py               # Core RAG logic (loading, embedding, QA)
├── main.py              # Streamlit UI
├── requirements.txt     # Python dependencies
├── .env                 # API keys (not committed)
└── resources/
    └── vectorstore/     # Persisted ChromaDB vector store
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd real-estate-project
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> Get your Groq API key from [https://console.groq.com](https://console.groq.com)

### 5. Run the App

```bash
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🚀 How to Use

1. **Enter URLs** — Paste up to 3 real estate listing URLs in the sidebar (URL 1, URL 2, URL 3).
2. **Process URLs** — Click the **"Process URL"** button. The app will:
   - Load and parse the page content
   - Split text into chunks (chunk size: 400)
   - Generate embeddings using HuggingFace
   - Store vectors in ChromaDB
3. **Ask Questions** — Type any question in the **"Question"** input field.
4. **View Answer & Sources** — The answer and its source references will be displayed on the main page.

---


Install with:

```bash
pip install -r requirements.txt
```

---

## 🔑 Key Configuration (rag.py)

| Variable | Value | Description |
|---|---|---|
| `Chunk_size` | `400` | Text chunk size for splitting |
| `Embedding_model` | `sentence-transformers/all-mpnet-base-v2` | HuggingFace embedding model |
| `VectorStore_DIR` | `resources/vectorstore` | Local path for ChromaDB persistence |
| `Collection_name` | `real_estate` | ChromaDB collection name |
| LLM Model | `llama-3.3-70b-versatile` | Groq LLM model |
| `temperature` | `0.9` | LLM creativity setting |
| `max_tokens` | `500` | Max tokens per LLM response |

---

## 🛠️ Troubleshooting

**Issue: `GROQ_API_KEY` not found**
- Ensure your `.env` file exists and contains the key.
- Make sure `load_dotenv()` is called before any API usage.

**Issue: ChromaDB errors on first run**
- The `resources/vectorstore/` directory will be created automatically.
- If you encounter corruption issues, delete the folder and reprocess the URLs.

**Issue: URL loading fails**
- Some sites block scrapers. Try different URLs or ensure the site is publicly accessible.

---

## 📄 License

This project is for educational and research purposes.