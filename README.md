# PDF to Text API Server

A FastAPI-based HTTP server for converting PDF documents to Markdown text using PyMuPDF4LLM.

## Setup

### Prerequisites
- Python 3.13+
- PyMuPDF4LLM for PDF processing

### Installation
```bash
python -m venv .venv
source .venv/bin/activate
uv sync
```

## Configuration

No special configuration required. The API runs on port 8000 by default.

## Running

```bash
source .venv/bin/activate
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

## Docker

### Building the Docker Image

```bash
# Build the image
docker build -t pdf2text-api .

# Or with a specific tag
docker build -t pdf2text-api:latest .
```

### Running with Docker

```bash
# Run the container
docker run -d \
  --name pdf2text \
  --restart unless-stopped \
  -p 8000:8000 \
  pdf2text-api

# Run with custom port
docker run -d \
  --name pdf2text \
  --restart unless-stopped \
  -p 3000:8000 \
  pdf2text-api

# Run interactively for debugging
docker run -it --rm \
  -p 8000:8000 \
  pdf2text-api
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  pdf2text:
    build: .
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: unless-stopped
```

### Docker Usage Notes

**Health Check**: The container includes a health check that verifies the API is responding. You can check the health status with:

```bash
# Check container health
docker ps

# View health check logs
docker inspect --format='{{json .State.Health}}' pdf2text
```

**Logs**: View application logs:

```bash
# Docker run logs
docker logs pdf2text
```

**Troubleshooting**:
- Ensure PDF files are valid and not corrupted
- Check that port 8000 is not already in use on the host
- For permission issues with temporary files, ensure `/tmp` is writable

## API Endpoints

### Health Check
```bash
GET /health
```
Returns server status.

Example response:
```json
{
  "status": "ok"
}
```

### Convert PDF to Markdown
```bash
POST /pdf2markdown
Content-Type: multipart/form-data
```
Upload a PDF file for conversion to Markdown text.

**Parameters:**
- `file`: PDF file to convert (multipart/form-data)

**Response:**
- Success: `{"text": "converted markdown text"}`
- Error: `{"error": "error description"}`

## Examples

```bash
# Basic PDF conversion
curl -X POST 'http://localhost:8000/pdf2markdown' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@document.pdf'

# Health check
curl 'http://localhost:8000/health'

# Test with invalid file type (returns error)
curl -X POST 'http://localhost:8000/pdf2markdown' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@document.txt'
```

## Features

- **PDF to Markdown Conversion**: Converts PDF documents to structured Markdown text
- **File Validation**: Ensures only PDF files are processed
- **Error Handling**: Comprehensive error handling with descriptive messages
- **Health Monitoring**: Built-in health check endpoint
- **Docker Support**: Full containerization with health checks
- **Temporary File Management**: Automatic cleanup of temporary files

## Supported File Types

- PDF documents (.pdf)

## Dependencies

- FastAPI: Web framework
- PyMuPDF4LLM: PDF processing and text extraction
- python-multipart: File upload handling
- uvicorn: ASGI server

## Development

```bash
# Install development dependencies
uv sync

# Run with auto-reload
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Run tests (if available)
uv run pytest
```

## License

[Add your license information here]