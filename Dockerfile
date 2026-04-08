# =========================
# Base Python image
# =========================

FROM python:3.10-slim

# =========================
# Working directory
# =========================

WORKDIR /app

# =========================
# Copy project files
# =========================

COPY . .

# =========================
# Install dependencies
# =========================

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

# =========================
# Expose API port
# =========================

EXPOSE 7860

# =========================
# Start FastAPI server
# =========================

CMD ["uvicorn","server.app:app","--host","0.0.0.0","--port","7860"]