FROM python:3.11-slim

#set envionment variables
#ENV PYTHONUNBUFFERED 1

# run this before copying requirements for cache efficiency
RUN pip install --upgrade pip

# Adding requirements file to current directory
# just this file first to cache the pip install step when code changes
COPY requirements.txt /requirements.txt

#install dependencies
RUN pip install -r /requirements.txt

# copy code itself from context to image
COPY ./app /app

WORKDIR /app

EXPOSE 8080

# run from working directory, and separate args in the json syntax
CMD ["gunicorn"  , "-b", "0.0.0.0:8080", "app:server"]
