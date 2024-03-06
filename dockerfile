# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /api
WORKDIR /api

# Copy the api directory contents into the container at /api
COPY . .

COPY .env /api

# Install any needed packages specified in /project-root/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install supervisord
RUN apt-get update && apt-get install -y supervisor

# Copy the supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose port 5000 for the Flask app (if needed)
EXPOSE 5000

# Run supervisord when the container launches
CMD ["/usr/bin/supervisord"]
