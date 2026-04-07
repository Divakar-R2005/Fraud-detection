import joblib
from xgboost import XGBClassifier
from sklearn.metrics import classification_report

class FraudTrainer:
    def __init__(self):
        # scale_pos_weight = count(negative) / count(positive)
        # For this dataset, fraud is rare, so we give the positive class more weight.
        self.model = XGBClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            scale_pos_weight=500, # Initial guess based on imbalance
            random_state=42
        )

    def train(self, X_train, y_train):
        print("Training model...")
        self.model.fit(X_train, y_train)

    def evaluate(self, X_test, y_test):
        predictions = self.model.predict(X_test)
        print("\nModel Evaluation:")
        print(classification_report(y_test, predictions))

    def save_model(self, path='models/fraud_model.pkl'):
        joblib.dump(self.model, path)
        print(f"Model saved to {path}")