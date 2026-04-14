cd smart-lock-api 
pip install -r requirements.txt
venv\Scripts\Activate
uvicorn main:app --reload

http://127.0.0.1:8000/docs