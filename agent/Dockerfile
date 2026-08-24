FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy the code as the `agent` package so relative imports resolve
# (uvicorn agent.main:app -> /app/agent/main.py)
COPY . ./agent/
CMD ["uvicorn", "agent.main:app", "--host", "0.0.0.0", "--port", "8000"]
