# Use the official Python image as the base image
FROM --platform=linux/amd64 python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install dependencies
# We first install pipenv and then use it to install the rest of the dependencies
RUN pip install --upgrade pip
RUN pip install pipenv

# Copy the Pipenv files into the container
COPY Pipfile Pipfile.lock ./

# Install python packages
RUN pipenv install --system --deploy

# Copy the rest of your application's code
COPY . .

# You may add commands to copy .env from .env.sample or use environment variables
# COPY .env.sample .env
# Or configure environment variables in your Docker command or docker-compose.yml

# Command to run the application
CMD ["pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0"]