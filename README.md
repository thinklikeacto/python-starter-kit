# 🚀 Python Microservice Starter Kit

A production-ready Python microservice boilerplate with clean architecture, multiple database support, and best practices built-in.

## ✨ Features

- **Clean Architecture**: Clear separation of concerns with layered architecture
- **Microservices Architecture**: Properly isolated services with their own configurations
- **Multiple Database Support**: Ready-to-use configurations for PostgreSQL, MongoDB, and Redis
- **API Development**: FastAPI with automatic OpenAPI documentation
- **Authentication**: JWT-based authentication system
- **Database Migrations**: Alembic for schema migrations
- **Optimized Docker Setup**: 
  - Multi-stage builds for smaller images
  - Alpine-based images for minimal footprint
  - Separate production and development dependencies
  - Health checks for all services
  - Proper service isolation and networking
- **Type Safety**: Type hints and Pydantic models throughout the codebase
- **Error Handling**: Centralized error handling and custom exceptions
- **Logging**: Structured logging configuration
- **Testing**: Pytest setup with fixtures and examples
- **API Versioning**: Built-in support for API versioning
- **CORS**: Configured Cross-Origin Resource Sharing
- **Environment Variables**: Environment-based configuration using python-dotenv
- **Git Workflow**: GitFlow branching model for better collaboration

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
├── services/              # Microservices
│   ├── postgres/         # PostgreSQL service
│   │   ├── config/      # PostgreSQL configuration
│   │   ├── init/        # Initialization scripts
│   │   └── docker/      # Service-specific Dockerfile
│   ├── mongodb/         # MongoDB service
│   │   ├── config/      # MongoDB configuration
│   │   ├── init/        # Initialization scripts
│   │   └── docker/      # Service-specific Dockerfile
│   └── redis/           # Redis service
│       ├── config/      # Redis configuration
│       └── docker/      # Service-specific Dockerfile
├── db/                    # Database migrations
├── tests/                # Test suite
├── .env                  # Environment variables
├── docker-compose.yml    # Docker services
├── Dockerfile           # Container definition
├── requirements.txt     # Development dependencies
└── requirements.prod.txt # Production dependencies
```

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

1. Python 3.11 or higher
2. Docker and Docker Compose
3. Git
4. PostgreSQL 14 or higher
5. MongoDB 6.0 or higher
6. Redis (optional)

### Installing MongoDB

#### macOS (using Homebrew):
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

#### Ubuntu:
```bash
# Import MongoDB public key
curl -fsSL https://pgp.mongodb.com/server-6.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg --dearmor

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Install MongoDB
sudo apt update
sudo apt install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

#### Windows:
1. Download MongoDB Community Server from [MongoDB Download Center](https://www.mongodb.com/try/download/community)
2. Run the installer and follow the installation wizard
3. Add MongoDB bin directory to system PATH
4. Create directory: `C:\data\db`
5. Start MongoDB service

## 🚀 Getting Started

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd python-starter-kit
   ```

2. Start the services using Docker Compose:
   ```bash
   docker-compose up -d
   ```

The API will be available at http://localhost:8000
API documentation will be at http://localhost:8000/docs

## 🔧 Configuration

Configuration is handled through environment variables and service-specific configuration files:

Key configurations:
- `APP_NAME`: Application name
- `ENV`: Environment (development/production)
- `DATABASE_URL`: PostgreSQL connection string
- `MONGODB_URL`: MongoDB connection string
- `REDIS_URL`: Redis connection string

Service-specific configurations:
- PostgreSQL: `services/postgres/config/`
  - `postgresql.conf`: Database configuration
  - `pg_hba.conf`: Access control
- MongoDB: `services/mongodb/config/`
  - `mongod.conf`: Database configuration
- Redis: `services/redis/config/`
  - `redis.conf`: Cache configuration

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

The project uses an optimized Docker setup with:

1. Multi-stage builds for smaller images
2. Alpine-based images for minimal footprint
3. Separate production and development dependencies
4. Health checks for all services
5. Proper service isolation and networking
6. Volume management for data persistence

Build and run the application using Docker:

```bash
# Build and start all services
docker-compose up -d

# Build specific service
docker-compose build app

# View logs
docker-compose logs -f app

# Stop all services
docker-compose down
```

## 🔍 Troubleshooting

Common issues and solutions:

1. **MongoDB Connection Error**:
   - Ensure MongoDB is running: `brew services list` (macOS) or `systemctl status mongod` (Linux)
   - Check MongoDB URL in `.env` file
   - Verify MongoDB port is not blocked by firewall

2. **PostgreSQL Connection Error**:
   - Ensure PostgreSQL is running
   - Verify database exists: `createdb starter_kit`
   - Check database URL in `.env` file

3. **Alembic Migration Error**:
   - Ensure database exists and is accessible
   - Check if previous migrations were applied: `alembic history`
   - Run migrations with verbose output: `alembic upgrade head --sql`

## 📦 Dependencies

Key dependencies used:
- FastAPI: Modern web framework
- SQLAlchemy: SQL toolkit and ORM
- Alembic: Database migration tool
- Pydantic: Data validation
- PyJWT: JWT token handling
- Motor: Async MongoDB driver
- Psycopg2: PostgreSQL driver
- Redis: Redis client
- Pytest: Testing framework

## 🤝 Contributing

We believe great software is built together! Whether you're fixing a bug, adding a feature, or improving documentation, your contributions are warmly welcomed and appreciated. Even if you're new to open source, we encourage you to jump in - every contribution counts, and we're here to help you succeed! Check out our issues labeled "good first issue" to get started.

### Git Workflow

We follow the GitFlow branching model for development:

#### Main Branches
- `main`: Production-ready code
- `develop`: Main development branch

#### Supporting Branches
- `feature/*`: New features (branch from `develop`)
- `release/*`: Release preparation (branch from `develop`)
- `hotfix/*`: Emergency fixes for production (branch from `main`)
- `bugfix/*`: Bug fixes (branch from `develop`)

#### Branch Naming Convention
- Features: `feature/my-feature-name`
- Bugfixes: `bugfix/issue-description`
- Releases: `release/1.0.0`
- Hotfixes: `hotfix/critical-issue`

#### Development Workflow
1. Create a new feature branch:
   ```bash
   git checkout develop
   git checkout -b feature/my-feature
   ```

2. Make your changes and commit using conventional commits:
   ```bash
   git commit -m "feat: add new feature"
   ```

3. Push your feature branch:
   ```bash
   git push origin feature/my-feature
   ```

4. Create a Pull Request to merge into `develop`

5. After review and approval:
   - Merge into `develop`
   - Delete feature branch

#### Release Process
1. Create a release branch:
   ```bash
   git checkout develop
   git checkout -b release/1.0.0
   ```

2. Version bump and final testing

3. Merge into `main` and `develop`:
   ```bash
   git checkout main
   git merge release/1.0.0
   git tag -a v1.0.0 -m "Release 1.0.0"
   
   git checkout develop
   git merge release/1.0.0
   ```

4. Delete release branch:
   ```bash
   git branch -d release/1.0.0
   ```

#### Commit Message Format
We use conventional commits format:
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:
```bash
feat(auth): add JWT authentication
fix(db): resolve connection timeout issue
docs(api): update endpoint documentation
```

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- FastAPI
- SQLAlchemy
- Alembic
- And all other open source libraries used in this project
