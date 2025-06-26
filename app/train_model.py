import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Sample data — replace this with more examples or load from compliment_training.json
data = [
    {"karma_growth": 40, "helpful_answers": 5, "last_compliment_days": 7, "should_generate_compliment": 1},
    {"karma_growth": 10, "helpful_answers": 1, "last_compliment_days": 2, "should_generate_compliment": 0},
    {"karma_growth": 35, "helpful_answers": 4, "last_compliment_days": 9, "should_generate_compliment": 1},
    {"karma_growth": 5,  "helpful_answers": 0, "last_compliment_days": 10, "should_generate_compliment": 0},
    {"karma_growth": 60, "helpful_answers": 7, "last_compliment_days": 3, "should_generate_compliment": 1},
    {"karma_growth": 15, "helpful_answers": 2, "last_compliment_days": 1, "should_generate_compliment": 0},
    {"karma_growth": 50, "helpful_answers": 6, "last_compliment_days": 6, "should_generate_compliment": 1}
]

df = pd.DataFrame(data)

X = df[["karma_growth", "helpful_answers", "last_compliment_days"]]
y = df["should_generate_compliment"]

# Train/test split (optional)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# Save the model
joblib.dump(clf, "model.pkl")
print("Model saved to app/model.pkl")