# 📄 Mini-RAG PDF Chatbot

A lightweight Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDFs and ask questions about their content using LangChain, Google Generative AI, FAISS, and Streamlit.

---

## 🚀 Features

- 📁 Upload and read multi-page PDF documents
- 🔍 Chunk text using RecursiveCharacterTextSplitter
- 🔗 Generate vector embeddings using **GoogleGenerativeAIEmbeddings**
- 🧠 Perform question answering with **ChatGoogleGenerativeAI**
- 🗂️ Store and retrieve chunks using **FAISS vector store**
- 🧪 Evaluate RAG pipeline with **RAGAS**
- 🌐 User-friendly interface using **Streamlit**

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| `LangChain` | Document loading, text splitting, chains, prompts |
| `Google Generative AI` | Embedding & LLM (via Gemini) |
| `FAISS` | Efficient vector similarity search |
| `PyPDF2` | Extract text from PDFs |
| `Streamlit` | Frontend interface |
| `RAGAS` | Evaluation of RAG pipeline |

![WhatsApp Image 2025-06-15 at 16 55 35_6e409c0b](https://github.com/user-attachments/assets/c1d4f442-8ae4-47ea-9a8a-bc8ce617a680)
