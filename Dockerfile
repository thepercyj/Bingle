# Dockerfile

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.9.13

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Allows docker to cache installed dependencies between builds
RUN pip install --upgrade pip
COPY Bingle/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
COPY . .


EXPOSE 8000

# runs the production server
ENTRYPOINT ["python", "Bingle/manage.py"]
CMD ["runserver", "0.0.0.0:8000"]