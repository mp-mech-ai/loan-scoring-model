FROM python:3.12-slim

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy source code, models and data
COPY src/ src/
COPY models/ models/
COPY data/ data/

# Copy dependency files first (for caching)
COPY pyproject.toml uv.lock ./

RUN pip install --upgrade pip \
    && pip install .


# Expose API port
EXPOSE 8000

# Run FastAPI with Uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]
