# Use an official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install UV (faster than pip)
RUN pip install uv

# Copy dependency files first (for layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync

# Copy the rest of the code
COPY . .

# FastAPI port
EXPOSE 8000

# Run the app (adjust for your main.py)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]