FROM python:3.12-slim

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install git-lfs
RUN apt-get update && \
    apt-get install -y git-lfs && \
    git lfs install && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency files first (for caching)
COPY pyproject.toml uv.lock ./

RUN pip install --upgrade pip \
&& pip install uv

# Copy source code, models and data
COPY src/ src/
COPY models/ models/
COPY data/ data/

RUN uv sync

# Expose API port
EXPOSE 7860

# Run FastAPI with Uvicorn
CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]
