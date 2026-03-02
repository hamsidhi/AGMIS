import pandas as pd
import numpy as np
from app.services.classification import classification_service

# Generate small synthetic dataset for initialization
data = {
    'attendance_pct': np.random.uniform(40, 100, 100),
    'internal_avg': np.random.uniform(30, 100, 100),
    'assignment_rate': np.random.uniform(20, 100, 100),
    'practical_score': np.random.uniform(50, 100, 100),
    'attendance_trend': np.random.choice([-1, 0, 1], 100),
    'prev_exam_score': np.random.uniform(40, 100, 100),
    'submission_consistency': np.random.uniform(0, 1, 100),
    'target_category': np.random.choice(['Excellent', 'Good', 'Average', 'At Risk', 'Critical'], 100)
}

df = pd.DataFrame(data)
print("Initializing model training...")
msg = classification_service.train_model(df)
print(msg)

# Test a prediction
test_student = [75, 70, 80, 85, 0, 65, 0.9] # Mock features
result = classification_service.predict(test_student)
print(f"Test Prediction: {result['category']}")