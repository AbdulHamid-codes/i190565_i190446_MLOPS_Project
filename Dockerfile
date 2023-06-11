# Use the official Python base image with Python 3.8
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application code into the container
COPY . .

# Expose the port on which the Flask app will run (change it if necessary)
EXPOSE 5001

# Define the command to run the Flask application
CMD ["python", "app.py"]
