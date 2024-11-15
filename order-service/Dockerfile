# Use Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose the Flask port
EXPOSE 5002

# Run the application
CMD ["python", "order_api.py"]
