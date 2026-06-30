import re
import pandas as pd
from typing import List

def clean_text(text: str) -> str:
    """Cleans raw text data by removing URLs, hashtags, mentions, special characters, and emojis."""
    if not isinstance(text, str):
        return ""
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove mentions (@user) and hashtags (#tag)
    text = re.sub(r'@\w+|#\w+', '', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_dataframe(df: pd.DataFrame, text_column: str) -> pd.DataFrame:
    """Applies preprocessing steps to the dataframe text column."""
    df['cleaned_text'] = df[text_column].apply(clean_text)
    return df

def load_mental_health_dataset(file_path: str) -> pd.DataFrame:
    """Loads mental health dataset from a given path."""
    return pd.read_csv(file_path)
