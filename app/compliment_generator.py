import json
import datetime
import joblib
from typing import Optional
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"
TEMPLATE_PATH = BASE_DIR / "templates.json"
MODEL_PATH = BASE_DIR / "model.pkl"

with open(CONFIG_PATH) as f:
    CONFIG = json.load(f)

with open(TEMPLATE_PATH) as f:
    TEMPLATES = json.load(f)

MODEL = joblib.load(MODEL_PATH)


def days_since(date_input) -> int:
    if not date_input:
        return 999
    if isinstance(date_input, datetime.date):
        date = date_input
    else:
        date = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
    return (datetime.date.today() - date).days


def extract_features(social_metrics: dict, history: dict) -> dict:
    return {
        "karma_growth": social_metrics.get("karma_growth", 0),
        "helpful_answers": social_metrics.get("helpful_answers", 0),
        "last_compliment_days": days_since(history.get("last_compliment_generated"))
    }


def predict_should_generate(features: dict) -> bool:
    input_vec = [[
        features["karma_growth"],
        features["helpful_answers"],
        features["last_compliment_days"]
    ]]
    return MODEL.predict(input_vec)[0] == 1


def pick_template(social_metrics: dict) -> Optional[dict]:
  
    if social_metrics.get("karma_growth", 0) >= 30:
        for t in TEMPLATES:
            if t["trigger"] == "karma_growth":
                return {
                    "message": t["template"],
                    "reason": "Karma boost",
                    "priority": "motivational"
                }

    if social_metrics.get("helpful_answers", 0) >= 3:
        for t in TEMPLATES:
            if t["trigger"] == "helpful_answers":
                tag = social_metrics.get("tags_followed", [""])[0]
                return {
                    "message": t["template"].replace("in 'internships'", f"in '{tag}'"),
                    "reason": "Peer upvotes + tag match",
                    "priority": "emotional"
                }

    if social_metrics.get("profile_completeness", 0) >= 85:
        for t in TEMPLATES:
            if t["trigger"] == "profile_completeness":
                return {
                    "message": t["template"] + "🔥",
                    "reason": "Profile improvement",
                    "priority": "confidence"
                }

    return None


def generate_compliment(user_payload: dict) -> Optional[dict]:
    features = extract_features(user_payload["social_metrics"], user_payload["history"])
    
    if features["last_compliment_days"] < CONFIG["compliment_cooldown_days"]:
        return None

    should_send = predict_should_generate(features)
    if not should_send:
        return None

    compliment = pick_template(user_payload["social_metrics"])
    return compliment
