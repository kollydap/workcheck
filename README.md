# README.md

# WorkCheck: Attendance Management System

WorkCheck is a modern employee attendance tracking system built with FastAPI, SQLAlchemy, and PostgreSQL. The system provides secure authentication, multiple check-in methods including QR code and NFC, geolocation verification, and comprehensive reporting.

## Features

- **Secure Authentication**: JWT-based authentication system
- **Multiple Check-in Methods**: Support for QR code, NFC, and manual check-in
- **Geolocation Verification**: Validate user location during check-in/check-out
- **Company Management**: Support for multiple companies
- **User Roles**: Admin and regular employee roles
- **Comprehensive Reporting**: Detailed attendance records and reports
- **API First**: Built with a modern API-first approach

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/workcheck.git
cd workcheck
```

2. Configure environment variables:

```bash
cp .env-example .env
# Edit .env with your preferred settings
```

3. Start the application:

```bash
docker-compose up -d
```

The API will be available at http://localhost:8000

## API Documentation

Once the application is running, you can access the OpenAPI documentation at:

- API Docs: http://localhost:8000/docs
- Alternative API Docs: http://localhost:8000/redoc

## Development

### Project Structure

```
workcheck/
├── app/                    # Main application
│   ├── api/                # API endpoints
│   ├── core/               # Configuration
│   ├── models/             # Database models
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic
│   └── utils/              # Utilities
├── tests/                  # Test suite
└── docker/                 # Docker configurations
```

### Running Tests

```bash
docker-compose exec app pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
