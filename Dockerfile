FROM python:3.9
WORKDIR /app
COPY requirements.txt .
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "bot.py"]