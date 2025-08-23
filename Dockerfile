FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    xvfb \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN GECKODRIVER_VERSION=0.34.0 && \
    wget -O /tmp/geckodriver.tar.gz "https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz" && \
    tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin && \
    rm /tmp/geckodriver.tar.gz

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DISPLAY=:99

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
