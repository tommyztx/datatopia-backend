# Use a base image with Python
FROM python:3.12-slim


# Install system dependencies required for pyodbc and ODBC Driver
RUN apt-get update && apt-get install -y \
    curl \
    unixodbc \
    unixodbc-dev \
    gcc \
    g++ \
    make \
    && curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update && ACCEPT_EULA=Y apt-get install -y \
    msodbcsql18 \
    && apt-get clean

# Copy the rest of the app's source code
COPY . .

# Set PYTHONPATH to include the app directory module for language.py
ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for Vercel to route traffic
EXPOSE 10000

# Run the app using Gunicorn (Flask production server)
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app.api:app"]
