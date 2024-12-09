# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install NGINX
RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Copy NGINX configuration
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Expose the port the Django app runs on
EXPOSE 3000
EXPOSE 80

# Run both NGINX and Django app using a process manager (e.g., supervisor)
CMD service nginx start && python manage.py runserver 0.0.0.0:3000