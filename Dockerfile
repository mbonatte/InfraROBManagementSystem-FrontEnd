# Use an official Python runtime as a parent image
FROM python:slim

# Set the working directory in the container
WORKDIR /pms

# Clone the Flask app repository from GitHub
RUN apt-get update && \
    apt-get install -y git && \
    git clone https://github.com/mbonatte/InfraROBManagementSystem-FrontEnd.git /pms

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run app.py when the container launches
CMD ["flask", "run"]