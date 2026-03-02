import pandas as pd
import numpy as np
from app.services.prediction import prediction_service

print("--- AGMIS Model Initializer ---")

# 1. Create fake data to teach the model
data = {
    'attendance': np.random.uniform(40, 100, 200),
    'prev_exam': np.random.uniform(30, 100, 200),
    'internal_avg': np.random.uniform(30, 100, 200),
    'assignment_rate': np.random.uniform(20, 100, 200),
    'trend': np.random.choice([-1, 0, 1], 200),
    'final_score': np.random.uniform(30, 100, 200)
}
df = pd.DataFrame(data)

def predict(self, student_features: list) -> dict:
        """
        Takes one student's data and returns the predicted score.
        Updated to use column names and avoid warnings.
        """
        if self.model is None:
            return {"error": "The model is not trained yet."}

        # 1. Define the exact column names used during training
        column_names = ['attendance', 'prev_exam', 'internal_avg', 'assignment_rate', 'trend']
        
        # 2. Convert the list into a tiny 1-row DataFrame with names
        input_df = pd.DataFrame([student_features], columns=column_names)
        
        # 3. Predict without warnings
        raw_prediction = self.model.predict(input_df)[0]
        
        # 4. Rest of the logic remains the same
        final_score = float(np.clip(raw_prediction, 0, 100))
        lower_range = max(0, final_score - self.mae_score)
        upper_range = min(100, final_score + self.mae_score)
        
        return {
            "predicted_score": round(final_score, 2),
            "confidence_interval": {
                "minus": round(lower_range, 2),
                "plus": round(upper_range, 2),
                "margin": round(self.mae_score, 2)
            },
            "predicted_category": self._get_category_from_score(final_score)
        }

# 2. Train and save
print("Training the prediction model...")
result = prediction_service.train_model(df)
print(f"✅ Success: {result}")