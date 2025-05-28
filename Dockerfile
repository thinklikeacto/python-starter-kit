# Stage 1: Build dependencies
FROM python:3.11-alpine AS builder

# Set working directory
WORKDIR /app

# Copy only production requirements
COPY requirements.prod.txt .

# Install build dependencies and create virtual environment
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    apk add --no-cache --virtual .build-deps \
        gcc \
        python3-dev \
        musl-dev && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.prod.txt && \
    apk del .build-deps

# Stage 2: Run
FROM python:3.11-alpine

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set working directory
WORKDIR /app

# Create non-root user
RUN adduser -D appuser

# Copy application
COPY . .

# Set ownership
RUN chown -R appuser:appuser /app

# Use virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Switch to non-root user
USER appuser

# Expose the port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 