from nrclex import NRCLex
from typing import Dict
import pandas as pd

NRC_EMOTIONS = ["fear", "anger", "anticipation", "trust", "surprise",
                "positive", "negative", "sadness", "disgust", "joy"]


def extract_nrc_features(text: str) -> Dict[str, float]:
    if not isinstance(text, str) or not text.strip():
        return {emotion: 0.0 for emotion in NRC_EMOTIONS}
    lex = NRCLex()
    lex.load_raw_text(text)
    scores = lex.affect_frequencies
    return {emotion: float(scores.get(emotion, 0.0)) for emotion in NRC_EMOTIONS}


def extract_nrc_features_batch(texts) -> pd.DataFrame:
    rows = [extract_nrc_features(t) for t in texts]
    return pd.DataFrame(rows, columns=NRC_EMOTIONS)


def extract_liwc_like_features(text: str, lexicon_dict_path: str = None) -> Dict[str, float]:
    return {}