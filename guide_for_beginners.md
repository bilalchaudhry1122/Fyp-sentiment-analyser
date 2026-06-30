# Beginner's Guide: How to Get Your API Credentials and Datasets

This guide provides simple, step-by-step instructions for non-technical users to set up the API keys, dataset files, and clinical references needed to run the project.

---

## 1. How to Get Reddit API Credentials

Reddit allows developers to read public posts for research. To get credentials, you need a standard Reddit account.

### Step-by-Step Instructions:
1. Open your web browser and log in to [Reddit](https://www.reddit.com/).
2. Go to the Developer Apps page: **[https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)**.
3. Scroll to the bottom of the page and click the button that says **"create app..."** (or **"create another app..."** if you already have one).
4. Fill in the fields exactly as follows:
   - **name**: `MindPulseApp` (or any name you prefer)
   - **App Type**: Select the **"script"** option (the first radio button). *Crucial: do not choose "web" or "installed".*
   - **description**: `Academic project for sentiment analysis` (optional)
   - **about url**: Leave blank
   - **redirect uri**: `http://localhost:8080` (this is a required placeholder; you do not need to host anything)
5. Click **"create app"**.
6. The app details will display. Copy the following items:
   - **Client ID**: This is the 14-character code located directly under the name of your app (under the text "personal use script").
   - **Client Secret**: This is the 27-character code labeled **"secret"** inside the app box.
   - **User Agent**: This is a simple identification name you make up for your app. Format it like: `MindPulse/1.0 by YOUR_REDDIT_USERNAME`.
7. Open [config/config.ini](file:///d:/Fyp/config/config.ini) in your text editor and paste these under the `[reddit]` section:
   ```ini
   [reddit]
   client_id = your_client_id_here
   client_secret = your_client_secret_here
   user_agent = your_user_agent_here
   ```

---

## 2. How to Get Twitter/X API Credentials

Twitter/X requires a developer account to access their API v2. You need a standard Twitter/X account to apply.

### Step-by-Step Instructions:
1. Visit the **[Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)** and log in with your Twitter/X account.
2. If you don't have a developer profile, follow the prompts to sign up for a **Free Developer Account**. You will need to write a short description of what you are doing (e.g., "Student project analyzing public sentiment for mental health awareness").
3. In the Developer Dashboard, click on **"Projects & Apps"** in the left navigation sidebar.
4. Click on **"Default Project"** or create a new Project. Inside that project, click on your app settings.
5. Go to the **"Keys and Tokens"** tab at the top.
6. Look for **"Bearer Token"** and click **"Generate"** (or **"Regenerate"** if you've already generated one).
7. Copy the long token string (it starts with `AAAAAAAAAAAAAAAAAAAA...`). Save this securely because it will only show once.
8. Open [config/config.ini](file:///d:/Fyp/config/config.ini) and paste it under the `[twitter]` section:
   ```ini
   [twitter]
   bearer_token = your_bearer_token_here
   ```

---

## 3. How to Download the Mental Health Dataset

We need a list of labeled posts (posts annotated with labels like "Depression" or "Anxiety") to train our machine learning model.

### Step-by-Step Instructions:
1. Open your browser and go to **[Kaggle](https://www.kaggle.com/)**. Sign up for a free account if you don't have one.
2. Search for the dataset: **"Sentiment Analysis of Mental Health Social Media Text"** (by user `kktoh1105` or similar).
   - Alternatively, search for the **"Sentimental Analysis for Mental Health"** dataset (by user `gargmanas`).
3. Click the **"Download"** button on the dataset page to download a `.zip` archive.
4. Locate the downloaded ZIP file on your computer and extract (unzip) it.
5. Inside the extracted files, locate the main spreadsheet file ending with `.csv` (usually named `Sentiment_Analysis_of_Mental_Health_Social_Media_Text.csv` or similar).
6. Copy this `.csv` file and paste it inside your project folder at: **[d:\Fyp\data\processed\](file:///d:/Fyp/data/processed/)**.
7. If your file is named something else, rename it to `mental_health_posts.csv` to keep it clean.

---

## 4. How to Create or Add RAG Reference Material

The RAG (Retrieval-Augmented Generation) system retrieves context from expert documents to display in the application. It supports **both simple text files (.txt) and PDF documents/books (.pdf)** (like DSM-5 guides, clinical textbooks, or counseling guides).

### Option A: Creating a Custom Text File (.txt)
1. Open the **Notepad** application (or any text editor) on your computer.
2. Paste or type paragraphs containing clinical symptom guides or helpline info. For example:
   ```text
   Depression Symptoms (DSM-5 Reference): Depressed mood most of the day, markedly diminished interest or pleasure in activities, fatigue or loss of energy, feelings of worthlessness, insomnia or hypersomnia, and difficulty concentrating.
   
   Anxiety Symptoms (DSM-5 Reference): Excessive anxiety and worry occurring more days than not for at least 6 months, restlessness, being easily fatigued, muscle tension, and sleep disturbances.
   
   Mental Health Helplines (Emergency Support): US: Call/text 988. Canada: Call/text 988. UK: Call 111. Always contact a certified professional for medical guidance.
   ```
3. Save the file as `reference_guidelines.txt`.
4. Copy this file and paste it directly inside: **[models/rag_knowledge_base/](file:///d:/Fyp/models/rag_knowledge_base/)**.

### Option B: Adding PDF Books or Manuals (.pdf)
1. Locate the PDF file of a clinical guide, research article, or DSM-5 handbook on your computer.
2. Copy the PDF file (e.g., `dsm5_extract.pdf`).
3. Paste it directly inside the RAG folder: **[models/rag_knowledge_base/](file:///d:/Fyp/models/rag_knowledge_base/)**.
*Note: The code will automatically use the `pypdf` library to extract, chunk, and index the text from your PDF file so it can search it page-by-page.*

---

## 5. How to Check if You Did it Correctly

Once you have done the steps above, run the automated checker script using your virtual environment terminal:
```bash
.venv\Scripts\python src/verify_config.py
```
If you configured everything correctly, the checkers will print checkmarks `[✔]` instead of empty brackets `[ ]`.
