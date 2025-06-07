FROM python:3.11-slim
RUN apt-get update && apt-get install -y \
    wget curl gnupg unzip fonts-liberation \
    libnss3 libatk-bridge2.0-0 libgtk-3-0 libxss1 libasound2 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 \
    libgbm1 libpango-1.0-0 libpangocairo-1.0-0 libxshmfence1 libxext6 libxfixes3 libxcursor1 \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir playwright && \
    playwright install --with-deps chromium
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
