FROM python:3.8.7-slim

RUN apt update && apt upgrade -y

# update python install packages
RUN pip3 install --upgrade pip 
RUN pip3 install wheel setuptools

# install project packages
ADD ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

ADD ./frontend/ /frontend

HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl -f / http://localhost:8080/
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "-w=10","--threads=1", "--worker-class=gthread", "frontend:app"]