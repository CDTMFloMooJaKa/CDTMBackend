# Swipe Republic Backend

## Quick Start

### Option 1: Using Python (requires Python 3.8+)

1. Clone this repository
2. (Recommended) Create a virtual environment (Conda can be used aswell):
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start the server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
   ```

### Option 2: Using Docker (recommended for team consistency)

1. Make sure you have Docker and Docker Compose installed
2. Clone this repository
3. Build and start the container:
   ```bash
   docker-compose up
   ```

## API Documentation

Once the server is running, you can access:
- API endpoint: http://localhost:8080
- Swagger UI documentation: http://localhost:8080/docs
- ReDoc documentation: http://localhost:8080/redoc

## Development

The server automatically reloads when you make changes to any Python file in the project.

### Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # Main FastAPI application
│   ├── config.py        # Application settings
│   ├── routers/         # API routes
│   │   ├── __init__.py
│   │   └── items.py     # Example CRUD routes
│   └── models/          # Pydantic models
│       ├── __init__.py
│       └── item.py      # Example data models
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
└── README.md           # Project documentation
```

### Adding New Routes

1. Create a new file in the `app/routers/` directory
2. Define your router and endpoints
3. Include your router in `app/main.py`

### Testing the API

You can use tools like curl, Postman, or the built-in Swagger UI to test your API endpoints.

Example:
```bash
# Get all items
curl -X GET http://localhost:8080/items

# Create a new item
curl -X POST http://localhost:8080/items -H "Content-Type: application/json" -d '{"name": "Test Item", "description": "This is a test item", "price": 9.99}'
```

## Troubleshooting

- **Port conflict**: If port 8080 is already in use, change the port in `docker-compose.yml` or in the uvicorn command.
- **Docker issues**: Make sure Docker is running and you have appropriate permissions.
- **Dependency issues**: Ensure you're using Python 3.8 or newer and have all dependencies installed.
