FROM python:3.11-slim

WORKDIR /app

# Install system dependencies needed to download and unpack Echidna
RUN apt-get update && apt-get install -y curl unzip

# Download, unpack, and install the Echidna binary for Linux
RUN curl -L https://github.com/crytic/echidna/releases/download/v2.2.7/echidna-2.2.7-aarch64-linux.tar.gz -o echidna.tar.gz && \
    tar -xzf echidna.tar.gz && \
    mv echidna /usr/local/bin/ && \
    rm echidna.tar.gz

# Copy and install Python dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Download the spaCy language model
RUN python -m spacy download en_core_web_sm

# Copy our application code
COPY ./app /app/app