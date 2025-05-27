# 🚀 Python Microservice Starter Kit

A production-ready Python microservice boilerplate with clean architecture, multiple database support, and best practices built-in.

## ✨ Features

- **Clean Architecture**: Clear separation of concerns with layered architecture
- **Multiple Database Support**: Ready-to-use configurations for PostgreSQL, MongoDB, and Redis
- **API Development**: FastAPI with automatic OpenAPI documentation
- **Authentication**: JWT-based authentication system
- **Database Migrations**: Alembic for schema migrations
- **Docker Support**: Containerization with Docker and Docker Compose
- **Type Safety**: Type hints and Pydantic models throughout the codebase
- **Error Handling**: Centralized error handling and custom exceptions
- **Logging**: Structured logging configuration
- **Testing**: Pytest setup with fixtures and examples
- **API Versioning**: Built-in support for API versioning
- **CORS**: Configured Cross-Origin Resource Sharing
- **Environment Variables**: Environment-based configuration using python-dotenv

## 🏗️ Project Structure

```
project/
├── app/                      # Main application logic
│   ├── api/                  # API layer (REST or gRPC)
│   │   ├── v1/              # API version 1
│   │   │   ├── routes/      # API endpoints
│   │   │   └── schemas/     # Request/Response models
│   │   └── dependencies.py  # FastAPI dependencies
│   ├── core/                # Core modules
│   │   ├── config.py       # Settings and configuration
│   │   ├── logger.py       # Logging setup
│   │   └── errors.py       # Custom exceptions
│   ├── models/             # Database models
│   ├── repository/         # Database operations
│   ├── services/          # Business logic
│   └── utils/             # Utility functions
├── db/                    # Database migrations
├── tests/                # Test suite
├── .env                  # Environment variables
├── docker-compose.yml    # Docker services
├── Dockerfile           # Container definition
└── requirements.txt     # Python dependencies
```

## 🚀 Getting Started

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd python-starter-kit
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

5. Start the services using Docker Compose:
   ```bash
   docker-compose up -d
   ```

6. Run database migrations:
   ```bash
   alembic upgrade head
   ```

7. Start the application:
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at http://localhost:8000
API documentation will be at http://localhost:8000/docs

## 🔧 Configuration

Configuration is handled through environment variables. See `.env.example` for available options.

Key configurations:
- `APP_NAME`: Application name
- `ENV`: Environment (development/production)
- `DATABASE_URL`: PostgreSQL connection string
- `MONGODB_URL`: MongoDB connection string
- `REDIS_HOST`: Redis host
- `SECRET_KEY`: Secret key for JWT tokens

## 📚 API Documentation

The API documentation is automatically generated and can be accessed at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

## 🧪 Testing

Run tests using pytest:
```bash
pytest
```

## 🐳 Docker

Build and run the application using Docker:

```bash
# Build the image
docker build -t python-starter-kit .

# Run with Docker Compose (recommended)
docker-compose up -d
```

## 📦 Dependencies

Key dependencies used:
- FastAPI: Modern web framework
- SQLAlchemy: SQL toolkit and ORM
- Alembic: Database migration tool
- Pydantic: Data validation
- PyJWT: JWT token handling
- Motor: Async MongoDB driver
- Redis: Redis client
- Pytest: Testing framework

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- FastAPI
- SQLAlchemy
- Alembic
- And all other open source libraries used in this project
