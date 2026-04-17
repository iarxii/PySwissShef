FROM python:3.11-slim

# Install system dependencies (For MSSQL and Graphviz)
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    unixodbc-dev \
    graphviz \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Microsoft ODBC Driver for SQL Server (Optionally needed for some scripts)
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Set working directory
WORKDIR /app

# Copy requirement list
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Pre-download NLP assets
RUN python -c "import nltk; nltk.download('vader_lexicon')"

# Expose Django port
EXPOSE 8000

# Entry point
CMD ["python", "main.py", "--web"]
