# Use an official Python image as base
FROM python:3.9

# Set the working directory
WORKDIR /app

COPY . .

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV DATABASE_URL=postgresql://hermeticum:secretpassword@postgres/journal_db

# Expose the FastAPI port
EXPOSE 8001


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]

