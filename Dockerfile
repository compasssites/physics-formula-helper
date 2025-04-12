# Use the official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy app files
COPY app.py formulas.csv requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit's default port
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]