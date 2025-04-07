# Flight Ticket Management System

A FastAPI-based backend system for managing flight tickets, schedules, and regulations.

## Features

- Employee authentication and authorization
- Flight schedule management
- Ticket sales and booking
- Regulation management
- Monthly reporting
- Employee performance tracking

## Prerequisites

- Python 3.8+
- PostgreSQL database
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd plane-be
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following variables:
```env
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=flight_tickets
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Initialize the database:
```bash
alembic upgrade head
```

## Running the Application

Start the server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- POST `/auth/register` - Register a new employee
- POST `/auth/token` - Login and get access token
- GET `/auth/me` - Get current user information

### Flights
- POST `/flights/` - Create a new flight
- GET `/flights/` - Get all flights
- GET `/flights/{flight_id}` - Get flight details
- PUT `/flights/{flight_id}` - Update flight
- DELETE `/flights/{flight_id}` - Delete flight

### Tickets
- POST `/tickets/` - Create a new ticket
- POST `/tickets/{ticket_id}/sell` - Sell a ticket
- GET `/tickets/` - Get all tickets
- GET `/tickets/{ticket_id}` - Get ticket details
- PUT `/tickets/{ticket_id}/cancel` - Cancel a ticket

### Regulations
- POST `/regulations/` - Create a new regulation
- GET `/regulations/` - Get all regulations
- GET `/regulations/{regulation_id}` - Get regulation details
- PUT `/regulations/{regulation_id}` - Update regulation
- PUT `/regulations/{regulation_id}/toggle` - Toggle regulation status

### Reports
- GET `/reports/monthly` - Get monthly report
- GET `/reports/sales` - Get sales report
- GET `/reports/employee-performance` - Get employee performance report

## Testing

Run tests with:
```bash
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
