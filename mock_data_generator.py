import csv
import random
import os

def generate_mock_csv(filename, batch_name, start_id, num_students, week):
    headers = [
        "student_id", "name", "week",
        "lecture_present", "lecture_total",
        "practical_present", "practical_total",
        "assignments_submitted", "assignments_total",
        "internal_marks", "external_marks", "practical_marks"
    ]
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for i in range(num_students):
            student_id = f"{start_id + i}"
            # Name must be consistent for the same student ID
            name = f"Student {batch_name} {i+1}"
            
            # Generate realistic varying stats for the week/subject context
            lec_total = 10
            lec_present = random.randint(3, 10)
            
            prac_total = 5
            prac_present = random.randint(1, 5)
            
            assign_total = 1
            assign_submitted = random.choice([0, 1])
            
            internal = random.randint(10, 20)
            external = random.randint(30, 75)
            prac_marks = random.randint(10, 25)
            
            row = [
                student_id, name, week,
                lec_present, lec_total,
                prac_present, prac_total,
                assign_submitted, assign_total,
                internal, external, prac_marks
            ]
            writer.writerow(row)

if __name__ == "__main__":
    import shutil
    
    # Clean up existing mock_data directory to avoid clutter if re-running
    if os.path.exists("mock_data"):
        shutil.rmtree("mock_data")
    
    os.makedirs("mock_data", exist_ok=True)
    
    SUBJECTS = [
        "Machine Learning", 
        "Data Governance", 
        "Computer Networks", 
        "Software Engineering", 
        "Database Systems"
    ]
    
    BATCHES = [
        {"name": "Year1_A1", "start_id": 1001, "num_students": 20},
        {"name": "Year1_B1", "start_id": 1021, "num_students": 20}
    ]
    
    WEEKS = [1, 2, 3]

    for batch in BATCHES:
        for subject in SUBJECTS:
            # Create a dedicated folder for each batch to keep things organized
            batch_folder = os.path.join("mock_data", batch["name"])
            os.makedirs(batch_folder, exist_ok=True)
            
            for week in WEEKS:
                safe_subj = subject.replace(" ", "_")
                filename = os.path.join(batch_folder, f"{batch['name']}_{safe_subj}_Week{week}.csv")
                
                generate_mock_csv(
                    filename=filename, 
                    batch_name=batch["name"], 
                    start_id=batch["start_id"], 
                    num_students=batch["num_students"], 
                    week=week
                )
                
    print(f"Successfully generated mock CSVs in the mock_data/ folder.")
    print(f"Total Combinations: {len(BATCHES)} batches x {len(SUBJECTS)} subjects x {len(WEEKS)} weeks.")
