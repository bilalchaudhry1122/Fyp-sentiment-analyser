import os
import torch
from transformers import AutoTokenizer, AutoModel

from src.data_preprocessing import clean_text, EMOTION_LABELS
from src.lexicon_feature_extraction import extract_nrc_features, NRC_EMOTIONS
from src.hybrid_model import HybridSentimentClassifier

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"
WEIGHTS_PATH = os.path.join("models", "roberta_finetuned", "best_hybrid_model.pt")

_device = "cuda" if torch.cuda.is_available() else "cpu"
_tokenizer = None
_roberta_model = None
_hybrid_model = None


def _load_models():
    """Lazy-loads all models once, on first prediction call."""
    global _tokenizer, _roberta_model, _hybrid_model
    if _hybrid_model is not None:
        return

    print("Loading RoBERTa tokenizer/model...")
    _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    _roberta_model = AutoModel.from_pretrained(MODEL_NAME).to(_device)
    _roberta_model.eval()

    print("Loading trained hybrid classifier...")
    _hybrid_model = HybridSentimentClassifier(roberta_dim=768, lexicon_dim=len(NRC_EMOTIONS), num_labels=len(EMOTION_LABELS))
    _hybrid_model.load_state_dict(torch.load(WEIGHTS_PATH, map_location=_device))
    _hybrid_model.to(_device)
    _hybrid_model.eval()
    print("Models loaded.")


@torch.no_grad()
def _get_roberta_embedding(text: str, max_length: int = 256):
    enc = _tokenizer([text], padding=True, truncation=True, max_length=max_length, return_tensors="pt").to(_device)
    out = _roberta_model(**enc)
    last_hidden = out.last_hidden_state
    mask = enc['attention_mask'].unsqueeze(-1).float()
    pooled = (last_hidden * mask).sum(1) / mask.sum(1).clamp(min=1e-9)
    return pooled  # shape (1, 768)


def predict(raw_text: str) -> dict:
    """Full pipeline: raw text -> cleaned -> lexicon + RoBERTa features -> hybrid model -> prediction."""
    _load_models()

    cleaned = clean_text(raw_text)
    if not cleaned:
        return {"error": "Text is empty after cleaning."}

    lex_scores = extract_nrc_features(cleaned)
    lex_vector = torch.tensor([[lex_scores[e] for e in NRC_EMOTIONS]], dtype=torch.float32).to(_device)

    roberta_vector = _get_roberta_embedding(cleaned)

    combined = torch.cat([roberta_vector, lex_vector], dim=1)

    with torch.no_grad():
        logits = _hybrid_model(combined)
        probs = torch.softmax(logits, dim=1).cpu().numpy()[0]

    pred_idx = int(probs.argmax())
    confidence_by_label = {EMOTION_LABELS[i]: round(float(probs[i]), 4) for i in range(len(EMOTION_LABELS))}

    return {
        "predicted_label": EMOTION_LABELS[pred_idx],
        "confidence": round(float(probs[pred_idx]), 4),
        "all_scores": confidence_by_label,
        "lexicon_scores": lex_scores,
        "cleaned_text": cleaned,
    }