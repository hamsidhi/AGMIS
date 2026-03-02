import pandas as pd
import io
from app.services.database import db_service
from app.services.features import feature_service
from app.services.classification import classification_service
from app.services.prediction import prediction_service
from app.services.guidance import guidance_service

class SystemIntegrator:
    """
    The 'General Manager' of AGMIS.
    This class connects all the services we built.
    """

    def process_faculty_upload(self, csv_file_contents: bytes):
        """
        1. Receives raw CSV data
        2. Saves it to Database
        3. Runs ML Models
        4. Saves Results
        """
        try:
            # Step 1: Read the CSV into a Pandas Table (DataFrame)
            df = pd.read_csv(io.BytesIO(csv_file_contents))
            
            # Step 2: Loop through every student in the file
            for index, row in df.iterrows():
                student_id = int(row['student_id'])
                
                # Step 3: Save the raw data to the Database (Step 9)
                db_service.insert_academic_record(
                    student_id=student_id,
                    attendance=row['attendance'],
                    internal=row['internal_marks'],
                    assignments=row['assignment_score']
                )
                
                # Step 4: Create 'Signals' for AI (Step 3)
                # Order: [attendance, prev_exam, internal_avg, assignment_rate, trend]
                features = [
                    row['attendance'], 
                    row['prev_exam'], 
                    row['internal_marks'], 
                    row['assignment_score'],
                    row['trend']
                ]
                
                # Step 5: Run the Crystal Ball (Step 5 - Prediction)
                prediction_result = prediction_service.predict(features)
                
                # Step 6: Save the prediction so the student can see it (Step 9)
                db_service.save_prediction(
                    student_id=student_id,
                    score=prediction_result['predicted_score'],
                    lower=prediction_result['confidence_interval']['minus'],
                    upper=prediction_result['confidence_interval']['plus']
                )
                
                # Step 7: Log the action
                print(f"✅ Processed student {student_id}: Predicted {prediction_result['predicted_score']}")

            return {"status": "success", "message": f"Processed {len(df)} students successfully."}

        except Exception as e:
            print(f"❌ Integration Error: {e}")
            return {"status": "error", "message": str(e)}

# Create the single manager instance
integrator = SystemIntegrator()