import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from typing import Dict, List, Any


class ClassificationService:
    def __init__(self):
        self.model_path = "models/student_classifier.joblib"
        self.model = None

        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)

    def train_model(self, data: pd.DataFrame):
        """
        Train Random Forest classifier (PRD 9.2.4)
        """

        X = data.drop(columns=["target_category"])
        y = data["target_category"]

        # split for evaluation
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=10,
            min_samples_leaf=5,
            max_features="sqrt",
            class_weight="balanced",
            random_state=42
        )

        model.fit(X_train, y_train)

        os.makedirs("models", exist_ok=True)
        joblib.dump(model, self.model_path)

        self.model = model
        return "Model trained and saved successfully."

    def predict(self, features: List[float]) -> Dict[str, Any]:
        if not self.model:
            raise Exception("Model not trained. Please train first.")

        feat_array = [features]

        prediction = self.model.predict(feat_array)[0]
        probabilities = self.model.predict_proba(feat_array)[0]

        classes = self.model.classes_
        confidences = {
            classes[i]: round(probabilities[i] * 100, 2)
            for i in range(len(classes))
        }

        return {
            "category": prediction,
            "confidence_scores": confidences,
            "logic": "Random Forest (200 trees)"
        }

    def get_feature_importance(self, feature_names: List[str]) -> Dict[str, float]:
        if not self.model:
            return {}

        importances = self.model.feature_importances_

        return {
            name: round(val, 4)
            for name, val in zip(feature_names, importances)
        }


classification_service = ClassificationService()
