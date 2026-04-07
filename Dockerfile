FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential default-libmysqlclient-dev pkg-config && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
EXPOSE 8501
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]