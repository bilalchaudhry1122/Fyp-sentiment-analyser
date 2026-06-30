# Project Status and Development Workflow

This document tracks the initialization progress, outlines current/future tasks, and specifies instructions for the user regarding configuration and credentials.

---

## 1. What Work is Done

### Codebase Skeleton & Directory Structure
We have created the standardized directory layout for development:
- **`data/`**: Subfolders `raw/`, `processed/`, and `lexicons/` for data storage.
- **`models/`**: Subfolders `roberta_finetuned/` and `rag_knowledge_base/` for saved models and indexes.
- **`notebooks/`**: Created for future exploratory analysis.
- **`config/`**: Contains `config.ini` template for secure configuration of paths and APIs.
- **`src/`**: Python module package containing script skeletons for all system modules:
  - `src/data_collection.py`: API retrieval skeletons.
  - `src/data_preprocessing.py`: Regex text cleaning skeletons.
  - `src/lexicon_feature_extraction.py`: Lexicon feature extraction using `nrclex`.
  - `src/roberta_finetuning.py`: Model loading and training loop skeletons.
  - `src/rag_system.py`: Vector retriever (FAISS) and augmenter class.
  - `src/hybrid_model.py`: Multi-modal neural classifier definition.
  - `src/model_evaluation.py`: Performance metrics calculation.
  - `src/app.py`: Flask application factory entrypoint.
  - `src/routes/views.py` & `src/routes/analyze.py`: Web routing blueprints.

### Premium Web Interface (Frontend UI)
A high-end, responsive, glassmorphic UI dashboard has been built using HTML5/vanilla CSS/JS:
- **`templates/base.html`**: Master layout with glowing orb backdrops, modern Outfit/Inter typography, and navigation bar.
- **`templates/index.html`**: Interactive analysis dashboard containing the input text form, character counters, sample loaders, diagnostic graphs, and RAG context displays.
- **`templates/results.html`**: Clean secondary results viewport for standalone reports.
- **`static/css/style.css`**: CSS stylesheet implementing a sleek slate-dark color palette, backdrop blurs, neon accent glows, and smooth transitions.
- **`static/js/analyze.js`**: Reacts dynamically to text input, fetches predictions from `/analyze` endpoint, displays progress indicators, highlights risk alerts, and animates scores.

### Project Brain Database (`project-brain/`)
Initialized the specialized Project Brain repository map to accelerate agent execution and limit token consumption:
- **`project-brain/graph/graph.json`**: Pre-seeded component dependencies.
- **`project-brain/memory/`**: 10 distinct memory files mapped by pipelines.
- **`project-brain/tasks/`** & **`cache/`**: Subfolders to track state, logs, and context dynamically.

### Git Version Control
- **Repository Initialized**: Created a local git repository, added custom `.gitignore` exclusions, and completed the baseline initial commit.

---

## 2. What is Undergoing (Underway)

- **Environment Verification (Succeeded)**: We successfully completed the re-installation of `torch==2.8.0+cpu`. The virtual environment is now fully verified and tested: `torch`, `transformers`, `nrclex`, `faiss`, and `flask` import successfully.
- **Awaiting User Action**: We are currently waiting for API configuration and source datasets (as detailed in Section 4) to proceed to development.

---

## 3. What is Remaining (Future Implementation Steps)

1. **Step 2 (APIs & Cleaning)**: Implement full Twitter/Reddit fetching code and configure dataset pipelines to read CSV records into processed frames.
2. **Step 3 (Lexicon Extraction)**: Integrate LIWC open-source alternative dictionaries and complete NRC emotion extraction mapping.
3. **Step 4 (Fine-Tuning)**: Build the PyTorch Dataset and trainer sequence to fine-tune `cardiffnlp/twitter-roberta-base-sentiment` or `roberta-base` on mental health datasets.
4. **Step 5 (RAG Database)**: Set up sentence embeddings, populate the FAISS index with psychological assessment documents, and write query similarity search functions.
5. **Step 6 (Hybrid Integration)**: Concatenate the RoBERTa embeddings, Lexicon scores, and RAG output, passing them through a trainable `HybridSentimentClassifier` layer.
6. **Step 7 (Evaluation)**: Train and validate the hybrid model, checking accuracy, precision, recall, and F1 metrics on cross-validation sets.
7. **Step 8 (Backend Flask API Integration)**: Bind the trained `HybridSentimentClassifier` weights and tokenizer into `src/routes/analyze.py` to replace placeholder stubs with live model output.

---

## 4. Things YOU (the User) Have to Do

> [!NOTE]
> If you are new to APIs, Kaggle, or configuring credentials, please see the step-by-step **[Beginner's Guide](file:///d:/Fyp/guide_for_beginners.md)** which explains exactly where to click, what to copy, and how to download these items.

To transition the project from skeletons to a fully functioning model, you must complete the following configuration steps:

### 1. API Credentials Configuration
We need developer keys to fetch raw testing data from Twitter and Reddit:
*   **Reddit API**:
    1. Go to [Reddit Apps Preferences](https://www.reddit.com/prefs/apps) (log in).
    2. Click **"create another app..."** or **"create app..."** at the bottom.
    3. Choose **"script"**. Give it a name (e.g., "MindPulse").
    4. Fill in `redirect uri` as `http://localhost:8080`.
    5. Copy the **Client ID** (the string under "personal use script") and the **Client Secret** (labeled "secret").
    6. Open [config.ini](file:///d:/Fyp/config/config.ini) and paste them under the `[reddit]` section.
*   **Twitter API**:
    1. Go to the [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard).
    2. Create a Project and an App under Twitter API v2.
    3. Retrieve the **Bearer Token**.
    4. Paste it under the `[twitter]` section in `config.ini`.

### 2. Source Labeled Datasets
To train the deep learning model (RoBERTa), we need labeled examples of mental health posts:
*   **Dataset Recommendation**: Download the "Sentiment Analysis of Mental Health Social Media Text" dataset from Kaggle (or a similar dataset that labels posts for depression/anxiety).
*   **Placement**: Save the `.csv` file directly under [data/processed/](file:///d:/Fyp/data/processed/) (e.g., `data/processed/mental_health_posts.csv`).

### 3. RAG Knowledge Reference Material
To support the Retriever (RAG) system with clinical insights:
*   **Instructions**: Create one or more text files containing paragraphs of expert guidelines (e.g., DSM-5 diagnostic criteria for depression/anxiety, mental health support numbers, or clinical counseling advice).
*   **Placement**: Save them as `.txt` files under [models/rag_knowledge_base/](file:///d:/Fyp/models/rag_knowledge_base/) (e.g., `models/rag_knowledge_base/guidelines.txt`).

### 4. Verify Your Configuration
Once you have done the steps above, run this script using your virtual environment to verify everything is correctly placed:
```bash
.venv\Scripts\python src/verify_config.py
```
This will print a checkmark table showing which credentials and files have been successfully loaded.
