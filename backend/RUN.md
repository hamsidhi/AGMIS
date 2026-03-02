# AGMIS Backend – Run from here

**Primary backend path:** `E:\Projects\agmis\backend`

## Run the app

**Option A – Double‑click:**  
Run **`run.ps1`** in this folder. The app will start on **http://127.0.0.1:8001**

**Option B – Terminal:**

1. Open a terminal and go to the backend folder:
   ```
   cd E:\Projects\agmis\backend
   ```
2. Activate the virtual environment:
   ```
   .\venv\Scripts\activate
   ```
3. Start the server (we use port **8001** to avoid conflict with other apps on 8000):
   ```
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
   ```
4. In the browser open: **http://127.0.0.1:8001**

## Web not loading?

- **Port in use:** If you see `[winerror 10048] only one usage of each socket address` then port 8000 (or 8001) is already in use. Either:
  - Close the other app (e.g. another terminal running uvicorn, or the “New folder” backend), or
  - Use a different port: `uvicorn app.main:app --reload --host 127.0.0.1 --port 8002` and open **http://127.0.0.1:8002**
- **Wrong folder:** You must run the command from `E:\Projects\agmis\backend`. If you run from `E:\Projects\agmis` or from `New folder\backend`, the app may not load or may be the wrong one.
- **Check server:** Open **http://127.0.0.1:8001/health** – you should see `{"status":"ok","message":"AGMIS is running"}`.

## CSV upload format (this backend only)

Required columns (any case):

- `student_id`, `name`, `week`
- `lecture_present`, `lecture_total`
- `practical_present`, `practical_total`
- `assignments_submitted`, `assignments_total`
- `internal_marks`, `external_marks`, `practical_marks`

Do **not** use the old schema (`student_number`, `subject_code`, `term`, `year`, `grade`). That is for a different backend. This one uses the columns above.

## If the app does not load

- Ensure you are running from `E:\Projects\agmis\backend` (this folder).
- Do not run from `E:\Projects\agmis\New folder\backend` or from `E:\Projects\agmis` without being in `backend`.
- Check the terminal for Python errors when starting.
