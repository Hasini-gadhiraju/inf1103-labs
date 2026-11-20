FROM python:3.11-slim

WORKDIR /app

# Copy every Python module needed by inventory_manager.py.
COPY . .

CMD ["python", "inventory_manager.py"]
