FROM python:3.12-slim

# Put the script in /app
WORKDIR /app
COPY . .

CMD ["python", "main.py"]