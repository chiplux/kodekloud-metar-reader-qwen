# Multi-stage build for smaller image size using Alpine for both stages

# Stage 1: Builder stage
FROM python:3.9-alpine AS builder

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev

# Create directory for dependencies
WORKDIR /install

# Copy production requirements file
COPY requirements-prod.txt .

# Install Python dependencies to a temporary directory
RUN pip install --no-cache-dir --prefix=/install -r requirements-prod.txt

# Stage 2: Runtime stage
FROM python:3.9-alpine

# Create non-root user with specific UID
RUN adduser -D -u 1001 metar-user

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Remove test files for production image
RUN rm -rf tests/ test_*.py *_test.py

# Change ownership to non-root user
RUN chown -R 1001:1001 /app

# Switch to non-root user
USER 1001

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Run the application
CMD ["python", "app.py"]