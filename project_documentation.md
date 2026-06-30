# Project Documentation & Working Guide

Welcome to the **Hybrid Lexicon-RoBERTa + RAG Social Media Analysis** project manual! This guide is written to help you understand what this project is about, how it works, what the codebase structure looks like, and what makes this system successful.

---

## 1. What is This Project About?

Social media posts (on platforms like Twitter/X and Reddit) can reveal a lot about a person's mental state. This project builds a tool that can analyze a social media post and determine if the author shows signs of psychological distress—specifically **depression, anxiety, or stress**—and classify their overall sentiment. 

If a post contains alarming mental health markers, the system will **flag** it for early intervention, enabling support platforms to reach out to the individual.

### The Hybrid Concept Explained
Instead of relying on just one AI technique, this system combines three independent layers to make highly accurate assessments:

1. **The Lexicon Layer (NRC/LIWC)**:
   - *What it is*: A "dictionary-based" approach.
   - *How it works*: It looks for specific words associated with emotions (e.g., counting words related to "sadness," "anger," "fear," or "joy"). This gives us a raw mathematical count of emotional words.
2. **The Deep Learning Layer (RoBERTa)**:
   - *What it is*: A modern Transformer AI model (pre-trained by Meta/Facebook on millions of tweets/posts).
   - *How it works*: Unlike a dictionary that just counts words, RoBERTa reads the context, sarcasm, and sentence structure. It understands that "I'm feeling down" means sadness, even if the word "sad" isn't used.
3. **The Retrieval-Augmented Generation (RAG) Layer**:
   - *What it is*: A local vector search engine.
   - *How it works*: When a user inputs a post, the system searches a local database of clinical guidelines, DSM-5 manuals, and medical examples. It retrieves the most relevant clinical text (e.g., diagnostic markers of burnout) and feeds it to the AI alongside the original post so the model has "expert knowledge" before classifying.

*By fusing these three elements—dictionary rules, contextual deep learning, and clinical reference material—the classifier gets the best of all worlds.*

---

## 2. The Development Workflow & Architecture

The data travels through the system following these sequential stages:

```
[ Raw Social Media APIs ] ──> [ Data Cleaning ] ──> [ Feature Extraction ] ──┐
                                                    - Lexicon word counts     │
                                                    - RoBERTa embeddings     ├──> [ Hybrid Classifier ] ──> [ Web Dashboard ]
                                                    - RAG retrieved guidelines│
```

1. **Collection**: Extracting posts from Twitter or Reddit based on target search words (e.g. "exhausted", "hopeless").
2. **Preprocessing**: Normalizing text (removing garbage characters, URLs, usernames like `@username`, and formatting lowercase).
3. **Feature Extraction**: Running the cleaned text through the Lexicon extractor, the RoBERTa tokenizer, and the RAG vector index search.
4. **Fusing & Predicting**: Passing the merged vectors to a neural network classification layer that assigns category scores (Low/Medium/High) and generates an alert flag if needed.
5. **UI Rendering**: Sending the output back to a browser dashboard that displays the results beautifully.

---

## 3. Folder Structure & Code Guide

Below is a map of where everything lives on your disk and what each file's job is:

```
d:\Fyp\
├── data/                       # Storage for data files
│   ├── raw/                    # Raw JSON/CSV posts from APIs
│   ├── processed/              # Cleaned text datasets ready for training
│   └── lexicons/               # NRC or LIWC emotion dictionary resource files
│
├── models/                     # Saved AI components
│   ├── roberta_finetuned/      # Stored weights of our custom fine-tuned RoBERTa model
│   └── rag_knowledge_base/     # Stored vector database (FAISS index) and text/PDF reference books
│
├── notebooks/                  # Interactive draft folders for testing algorithms
│
├── src/                        # Core Python code pipeline
│   ├── __init__.py             # Makes python recognize 'src' as a code package
│   ├── verify_config.py        # Helper tool to test and check your keys and datasets configuration
│   ├── data_collection.py      # Authenticates and pulls posts from Twitter and Reddit APIs
│   ├── data_preprocessing.py   # Cleans text by removing URLs, HTML, and extra whitespace
│   ├── lexicon_feature_extraction.py # Extracts emotion counts using NRCLex
│   ├── roberta_finetuning.py   # Trains the base RoBERTa model on annotated datasets
│   ├── rag_system.py           # Embeds medical documents/PDFs and retrieves matching guidelines
│   ├── hybrid_model.py         # Defines the combined neural network classifier
│   ├── model_evaluation.py     # Calculates accuracy, precision, recall, and F1 performance
│   └── app.py                  # Launches the Flask web server
│
├── templates/                  # Frontend HTML web layouts
│   ├── base.html               # Shared layout header, navigation, and background glows
│   ├── index.html              # Main input page containing the text area and diagnostic panels
│   └── results.html            # Static secondary display page
│
├── static/                     # Frontend visual styling assets
│   ├── css/style.css           # Glassmorphic dark styling sheet, neon colors, animations
│   └── js/analyze.js           # Handles input events, contacts server API, and updates graphs
│
├── config/                     # Configuration
│   └── config.ini              # Template configuration for API credentials and paths
│
├── .venv/                      # Private virtual environment containing Python, torch, and packages
├── requirements.txt            # Package dependencies list (torch, transformers, flask, pypdf, etc.)
├── project_status_and_workflow.md # Status checklist detailing what we are working on
├── setup_report.md             # Verification report confirming environment imports
├── guide_for_beginners.md      # Detailed step-by-step setup manual for credentials & datasets
├── simplified_folder_guide.md  # A very simple guide explaining folders using a restaurant analogy
└── project_documentation.md    # This document!
```

---

## 4. How the Code Works (Step-by-Step Flow)

When a user pastes a paragraph into the web application, here is exactly what happens behind the scenes:

1. **The Click**: The user clicks **"Analyze Context"** on the webpage.
2. **JavaScript Fetch**: `static/js/analyze.js` intercepts the form submission, triggers a loading spinner, and sends the text in a JSON request to the Flask server endpoint: `/analyze` (configured in `src/routes/analyze.py`).
3. **Preprocessing**: The server runs `src/data_preprocessing.py` to strip out junk characters, web links, or weird symbols.
4. **Lexicon Extract**: The server runs `src/lexicon_feature_extraction.py` using `nrclex` to extract scores for 10 emotional classes (fear, sadness, anger, joy, trust, surprise, disgust, anticipation, positive, negative).
5. **RAG Context Retrieval**: The server runs `src/rag_system.py`. It converts the input text into a search vector, queries the local FAISS database, retrieves matching professional paragraphs (e.g., DSM-5 advice), and formats them.
6. **RoBERTa Context Vector**: The server loads the fine-tuned RoBERTa model (`src/roberta_finetuning.py`), tokenizes the text, and extracts the contextual semantic vector representing the sentence meaning.
7. **Hybrid Classifier Prediction**: The server merges these vectors into the classifier defined in `src/hybrid_model.py`. The model evaluates the composite data and outputs:
   - Predicted Sentiment (Positive, Negative, or Neutral)
   - Risk indicators for Depression (Low, Medium, or High)
   - Risk indicators for Anxiety (Low, Medium, or High)
   - Risk indicators for Stress (Low, Medium, or High)
   - Flag Alert: A boolean (`True` or `False`) indicating whether immediate clinical attention is advised.
8. **UI Display**: The Flask server returns this structured dictionary back to the webpage. The JavaScript parses the dictionary, dynamically scales the progress bars (coloring them green, yellow, or red), displays a warning banner if flagged, and displays the retrieved expert RAG advice.

---

## 5. How This Project Gets Successful

To make this project successful, you and the development assistant (me) must complete these integration phases:

1. **Proper API Access**: Input valid developer tokens into [config.ini](file:///d:/Fyp/config/config.ini) to allow fetching genuine training posts.
2. **Quality Training Data**: Obtain a high-quality labeled dataset (like the Reddit Mental Health dataset from Kaggle) and store it in `data/processed/` to train the RoBERTa model.
3. **Rigorous Fine-Tuning**: Fine-tune the RoBERTa model on this data until it achieves high accuracy on classifying sentiment and mental health states.
4. **Rich RAG Reference Library**: Populate `models/rag_knowledge_base/` with high-quality medical and psychological guidelines. The better the retrieved material, the more helpful the RAG advice displays.
5. **Clean Interface Execution**: Ensure the web dashboard is responsive, visually compelling, and presents results in an easily interpretable manner.

---

## 6. Things YOU (the User) Have to Do

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

---

## 7. Keeping Track

As we write new code, train the models, and deploy the application, **this document and [project_status_and_workflow.md](file:///d:/Fyp/project_status_and_workflow.md) will be updated continuously** to detail which functions have been written and what steps you need to perform next.
