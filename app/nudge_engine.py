import json
import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"

with open(CONFIG_PATH) as f:
    CONFIG = json.load(f)


def days_since(date_input) -> int:
    if not date_input:
        return 999
    if isinstance(date_input, datetime.date):
        date = date_input
    else:
        date = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
    return (datetime.date.today() - date).days

def compute_inactivity_score(buddy: dict) -> int:
    return (
        buddy.get("last_interaction_days", 0)
        + buddy.get("karma_change_7d", 0)  # may be negative
        - buddy.get("messages_sent", 0)
    )


def generate_buddy_nudges(user_payload: dict) -> list:
    nudges = []
    max_nudges = CONFIG["max_nudges_per_user"]
    idle_threshold = CONFIG["buddy_nudge_idle_days"]
    last_nudge_days = days_since(user_payload["history"].get("last_buddy_nudge", ""))

    if last_nudge_days < 3:
        # Don't nudge anyone if buddy nudge was sent < 3 days ago
        return []

    for buddy in user_payload.get("buddies", []):
        if buddy["last_interaction_days"] < idle_threshold:
            continue  # Buddy is active

        score = compute_inactivity_score(buddy)
        if score > CONFIG["karma_drop_threshold"]:
            nudges.append({
                "buddy_id": buddy["buddy_id"],
                "message": f"Your buddy {buddy['buddy_id']} has been quiet lately. Drop a message to cheer them up?",
                "priority": "gentle"
            })

        if len(nudges) >= max_nudges:
            break

    return nudges
