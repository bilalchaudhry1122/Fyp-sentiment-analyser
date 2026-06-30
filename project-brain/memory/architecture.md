# System Architecture

## Core Flow
1. **Data Source**: Social Media posts (Reddit, Twitter/X).
2. **Collection**: PRAW & Tweepy APIs saving raw text.
3. **Preprocessing**: Removing noise (URLs, @mentions, hashtags), tokenizing, normalizing, and handling slang.
4. **Lexicons**: Running NRC Emotion Lexicon and LIWC-like dictionary feature extraction.
5. **Context Augmentation (RAG)**: Embedding and index checking using FAISS vector store. Retrieving medical guidelines and expert assessments.
6. **Transformer Feature Extraction**: Contextualized embeddings from fine-tuned RoBERTa model.
7. **Hybrid Integration**: Concatenating lexicon scores + RoBERTa embeddings + RAG contextual features.
8. **Classification Layer**: Dense neural layers mapping combined features to Sentiment & Psychological state (Anxiety, Depression, Stress levels).
9. **Web App**: Flask dashboard allowing end-user diagnostics and risk-flagging.
