#FROM python:3.10-slim
FROM python:3.9


# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app


CMD ["python3", "-m", "uvicorn", "search:app","--reload", "--host", "127.0.0.1", "--port", "8000"]