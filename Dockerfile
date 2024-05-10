# Dockerfile

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.9.13

# Allows docker to cache installed dependencies between builds
COPY Bingle/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
COPY . app
WORKDIR /app

EXPOSE 8000

# runs the production server
ENTRYPOINT ["python", "Bingle/manage.py"]
CMD ["runserver", "0.0.0.0:8000d"]