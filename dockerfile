# Python runtime image
FROM python:3.12

# Set working directory to /app
WORKDIR /app

# Add the current directory contents into /app
ADD . /app

# Install packages 
RUN pip install --no-cache-dir -r requirements.txt

# set environment variables
ENV BOT_NAME="SET IT HERE"
ENV BOT_TOKEN="SET IT HERE"
ENV API_HASH="SET IT HERE"
ENV API_ID="SET IT HERE"

ENV GOOGLE_API_KEY="SET IT HERE"

# Run main.py when the container launches
CMD ["python", "main.py"]