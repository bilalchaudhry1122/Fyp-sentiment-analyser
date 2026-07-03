from flask import Blueprint, request, jsonify
from src.inference import predict

bp = Blueprint('analyze', __name__, url_prefix='/analyze')


def _prob_to_level(prob: float) -> str:
    """Converts a 0-1 class probability into a Low/Medium/High label for the UI."""
    if prob >= 0.66:
        return "High"
    elif prob >= 0.33:
        return "Medium"
    return "Low"


def _emotion_to_sentiment(label: str) -> str:
    """Coarse sentiment bucket derived from the psychological-state prediction."""
    if label == "Happy/Positive":
        return "Positive"
    if label == "Neutral":
        return "Neutral"
    return "Negative"  # Anxious/Stress or Depressed/Sad


@bp.route('', methods=['POST'])
def analyze_text():
    """Endpoint for hybrid text sentiment & psychological analysis."""
    data = request.get_json() or {}
    text = data.get('text', '')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = predict(text)
    if "error" in result:
        return jsonify(result), 400

    scores = result["all_scores"]
    predicted_label = result["predicted_label"]
    confidence = result["confidence"]

    # NOTE: the model was trained on a single combined "Anxious/Stress" class,
    # so anxiety and stress currently share the same underlying probability.
    depression_prob = scores.get("Depressed/Sad", 0.0)
    anxiety_stress_prob = scores.get("Anxious/Stress", 0.0)

    psychological_states = {
        "depression": _prob_to_level(depression_prob),
        "anxiety": _prob_to_level(anxiety_stress_prob),
        "stress": _prob_to_level(anxiety_stress_prob),
    }

    # Flag for early-awareness if the model is reasonably confident about a
    # concerning state (Objective 2 territory, wired in now since the signal exists)
    is_concerning = predicted_label in ("Anxious/Stress", "Depressed/Sad")
    flagged = is_concerning and confidence >= 0.5

    if not is_concerning:
        risk_level = "None"
    elif confidence >= 0.75:
        risk_level = "High"
    elif confidence >= 0.5:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    response_data = {
        "text": text,
        "sentiment": _emotion_to_sentiment(predicted_label),
        "sentiment_score": confidence,
        "predicted_label": predicted_label,
        "all_scores": scores,
        "psychological_states": psychological_states,
        "flagged": flagged,
        "risk_level": risk_level,
    }
    return jsonify(response_data)