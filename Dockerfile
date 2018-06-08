# Base Python image
FROM python:3.6-jessie

# Install pytwask and the WSGI server gunicorn via pip.
RUN pip install gunicorn pytwask
