
from app import create_app, db
from app.models import Task

app = create_app()

with app.app_context():
    try:
        # Try to query the Tasks table to ensure it connects
        tasks = Task.query.all()
        print("Connection Successful. Retrieved tasks:", tasks)
    except Exception as e:
        print("Error connecting to the database:", e)
