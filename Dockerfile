# Base image
FROM openjdk:8-jdk-slim

# Install Python and necessary packages
RUN apt-get update && apt-get install -y python3 python3-pip

# Install PySpark
# RUN pip3 install pyspark

# # Set environment variables for PySpark
# ENV PYSPARK_PYTHON=python3
# ENV PYSPARK_DRIVER_PYTHON=python3

# Copy requirements.txt if needed
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy your Python script into the container
COPY urban_with__pandas.py .

# Set the default command to run the Python script
CMD ["python3", "urban_with__pandas.py"]
