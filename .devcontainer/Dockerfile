FROM python:3.12.10-slim

# Set the working directory
WORKDIR /usr/src/app

# Update pip to the latest version
RUN pip install --upgrade pip

# Copy the requirements file into the container
COPY requirements.txt ./

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY src/ ./src/
