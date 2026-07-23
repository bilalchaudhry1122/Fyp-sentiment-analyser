import os
import re
import json
import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
from nrclex import NRCLex

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"

# All model files sit at the repo root (adjust if you move them into a subfolder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root, since this file lives in src/
WEIGHTS_PATH = os.path.join(BASE_DIR, "best_hybrid_model.pt")
LABEL_MAP_PATH = os.path.join(BASE_DIR, "label_mapping.json")
TOKENIZER_PATH = os.path.join(BASE_DIR, "tokenizer")
MAX_LEN = 256

NRC_EMOTIONS = ["fear", "anger", "anticipation", "trust", "surprise",
                "positive", "negative", "sadness", "disgust", "joy"]

_device = "cuda" if torch.cuda.is_available() else "cpu"
_tokenizer = None
_model = None
_emotion_labels = None


class HybridRobertaLexicon(nn.Module):
    """Must match the architecture used during training in Colab exactly."""
    def __init__(self, model_name, lexicon_dim=10, num_labels=4):
        super().__init__()
        self.roberta = AutoModel.from_pretrained(model_name)
        self.classifier = nn.Sequential(
            nn.Linear(768 + lexicon_dim, 256),
            nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(), nn.Dropout(0.2),
            nn.Linear(128, num_labels)
        )

    def forward(self, input_ids, attention_mask, nrc_feats):
        out = self.roberta(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden = out.last_hidden_state
        mask = attention_mask.unsqueeze(-1).float()
        pooled = (last_hidden * mask).sum(1) / mask.sum(1).clamp(min=1e-9)
        combined = torch.cat([pooled, nrc_feats], dim=1)
        return self.classifier(combined)


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#(\w+)', r'\1', text)
    text = re.sub(r'([!?.,])\1+', r'\1', text)
    return re.sub(r'\s+', ' ', text).strip()


def extract_nrc_features(text: str) -> dict:
    if not text.strip():
        return {e: 0.0 for e in NRC_EMOTIONS}
    lex = NRCLex()
    lex.load_raw_text(text)
    scores = lex.affect_frequencies
    return {e: float(scores.get(e, 0.0)) for e in NRC_EMOTIONS}


def _load_models():
    """Lazy-loads tokenizer, label map, and the fine-tuned hybrid model once."""
    global _tokenizer, _model, _emotion_labels
    if _model is not None:
        return

    print("Loading label mapping...")
    with open(LABEL_MAP_PATH) as f:
        label_data = json.load(f)
    _emotion_labels = label_data["EMOTION_LABELS"]

    print("Loading tokenizer...")
    _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    print("Loading fine-tuned hybrid model weights...")
    _model = HybridRobertaLexicon(MODEL_NAME, lexicon_dim=len(NRC_EMOTIONS), num_labels=len(_emotion_labels))
    _model.load_state_dict(torch.load(WEIGHTS_PATH, map_location=_device))
    _model.to(_device)
    _model.eval()
    print("Models loaded.")


def predict(raw_text: str) -> dict:
    """Full pipeline: raw text -> cleaned -> tokenized + lexicon features -> hybrid model -> prediction."""
    _load_models()

    cleaned = clean_text(raw_text)
    if not cleaned:
        return {"error": "Text is empty after cleaning."}

    lex_scores = extract_nrc_features(cleaned)
    lex_vector = torch.tensor([[lex_scores[e] for e in NRC_EMOTIONS]], dtype=torch.float32).to(_device)

    enc = _tokenizer(
        cleaned, truncation=True, padding='max_length',
        max_length=MAX_LEN, return_tensors='pt'
    ).to(_device)

    with torch.no_grad():
        logits = _model(enc['input_ids'], enc['attention_mask'], lex_vector)
        probs = torch.softmax(logits, dim=1).cpu().numpy()[0]

    pred_idx = int(probs.argmax())
    confidence_by_label = {_emotion_labels[i]: round(float(probs[i]), 4) for i in range(len(_emotion_labels))}

    return {
        "predicted_label": _emotion_labels[pred_idx],
        "confidence": round(float(probs[pred_idx]), 4),
        "all_scores": confidence_by_label,
        "lexicon_scores": lex_scores,
        "cleaned_text": cleaned,
    }


if __name__ == "__main__":
    tests = [
        "just got back from the gym feeling amazing today",
        "cant stop worrying about my exam tomorrow, my chest feels tight",
        "nothing feels worth it anymore, I just want to sleep all day",
    ]
    for t in tests:
        result = predict(t)
        print(f"{t!r} -> {result['predicted_label']} ({result['confidence']:.2%})")