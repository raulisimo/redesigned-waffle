# Use the official Python image as the base image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY ./requirements.txt /app/requirements.txt

# Install any dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the project files to the container
COPY . /app

# Expose the port that the application is listening on
EXPOSE 8080

# Set the entrypoint to run the application with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
