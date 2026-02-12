# Use Python 3.12 as base image
FROM python:3.12.3-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY ./app.py /app/app.py
COPY ./templates /app/templates
COPY ./requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]