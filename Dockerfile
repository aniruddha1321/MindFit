FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libjpeg-dev \
    zlib1g-dev

RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app
CMD ["streamlit", "run", "FinalProject.py"]
