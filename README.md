# Darukaa.Earth: AI Biodiversity Intelligence Chatbot

An AI-powered conversational environmental scientist designed to generate evidence-backed, multi-metric recommendations for improving biodiversity. This system moves beyond generic LLM responses by utilizing a hybrid knowledge layer (RAG + Structured SQL) and a rule-based multi-metric reasoning engine.

## 📸 Demo Screenshot
![Darukaa AI Demo](demo.png)
*(Upload a screenshot of your working Streamlit UI as `demo.png` in the root folder)*

## ✨ Key Features
- **Hybrid Knowledge Retrieval:** Combines ChromaDB (unstructured PDFs) with SQLite (structured metrics).
- **Multi-Metric Reasoning:** Connects at least 3 environmental variables per recommendation.
- **Slot-Filling Conversational Memory:** Asks clarifying questions and remembers context across turns.
- **Evidence-Backed Output:** Every recommendation includes measurable impact estimates, time horizon, and citations (FAO, IPCC, IPBES).

## 🏗️ System Architecture
The system is built on a modular architecture to ensure clear separation of concerns:

1. **Frontend (Streamlit):** Provides a chat interface for text queries and a sidebar for structured environmental data input.
2. **Backend (FastAPI):** Handles API routing, manages conversational memory, and orchestrates the reasoning pipeline.
3. **Hybrid Knowledge Layer:**
   - **Unstructured (RAG):** ChromaDB vector database containing indexed scientific reports (FAO, IPCC, IPBES) using `all-MiniLM-L6-v2` embeddings.
   - **Structured (SQL):** SQLite database (`sites.db`) storing numerical environmental metrics.
4. **Reasoning Engine:** A Python-based rule engine that generates non-obvious, scientifically grounded advice.
5. **Data Ingestion Pipeline:** Scripts to fetch real geospatial soil data (SoilGrids API), seed the database, and ingest scientific PDFs.

## 🗄️ Database Schema
The structured data is stored in SQLite (`db/schema.sql`). Key tables include:
- `sites`: Stores environmental metrics (`soil_ph`, `organic_carbon_pct`, `rainfall_mm`, `land_use`, `species_richness`, `region`, etc.).
- `documents`: Stores metadata for indexed scientific reports.
- `recommendations`: Logs generated recommendations for auditing.

## 💻 Tech Stack
- **Language:** Python 3.11
- **Backend:** FastAPI, Uvicorn
- **Frontend:** Streamlit
- **AI/ML:** LangChain, HuggingFace (Sentence-Transformers), ChromaDB
- **Database:** SQLite

## 🚀 Local Setup Instructions
Follow these steps to run the project locally:

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd darukaa-earth-ai

2.**Create and activate a virtual environment:**

bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

3.**Install dependencies:**

bash
pip install -r requirements.txt

4.**Fetch real soil data and seed the database:**

bash
python fetch_soil.py
python db/seed.py

5.**Ingest scientific PDFs into the vector database:**
Place your downloaded PDFs (FAO, IPCC, IPBES) inside the data/documents/ folder first.

bash
python rag/ingest.py

6.**Run the Backend API (Terminal 1):**

bash
uvicorn main:app --reload

7.**Run the Frontend UI (Terminal 2):**

bash
streamlit run app.py
Open your browser to the URL provided by Streamlit (usually http://localhost:8501).


🔄 CI/CD Details
This repository uses GitHub Actions for Continuous Integration.

The workflow is defined in .github/workflows/ci.yml.

On every push or pull request to the main branch, the action will:

Set up a Python 3.11 environment.
Install all dependencies from requirements.txt.
Verify that all Python files compile successfully without syntax errors.


📝 Notes on Data Sourcing
Since the hackathon did not provide a proprietary dataset, this system was designed with a plug-and-play architecture. The knowledge base was populated using publicly available scientific reports from the FAO, IPCC, and IPBES, and real geospatial soil data was fetched using the ISRIC SoilGrids API. The pipeline is designed to accept any proprietary CSV or PDF dataset without changing the core codebase.