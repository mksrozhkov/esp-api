run-debug:
	poetry run uvicorn --host localhost --port 8000 src.main:app --reload
