# Bitespeed Identity Reconciliation API

A FastAPI-based REST API for contact identity reconciliation and management. This application helps identify and link contacts based on their email addresses and phone numbers.

## Features

- **Contact Identification**: Identify contacts by email or phone number
- **Automatic Linking**: Automatically link related contacts into networks
- **Primary/Secondary Contact Management**: Maintain primary and secondary contact relationships
- **Network Expansion**: Recursively expand contact networks to find all related contacts
- **RESTful API**: Clean, RESTful API design with proper error handling

## Project Structure

```
Identity Reconciliation/
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Application configuration
│   │   └── db.py             # Database connection and session management
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py         # SQLAlchemy database models
│   ├── routes/
│   │   ├── __init__.py
│   │   └── routes.py         # API route definitions
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── schemas.py        # Pydantic request/response models
│   └── services/
│       ├── __init__.py
│       └── crud.py           # Database operations and business logic
├── main.py                   # FastAPI application entry point
├── requirements.txt          # Python dependencies
├── pyproject.toml           # Poetry configuration
├── poetry.lock              # Poetry lock file
├── .env                     # Environment variables (create this)
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Identity Reconciliation"
   ```

2. **Install dependencies**
   ```bash
   # Using pip
   pip install -r requirements.txt
   
   # Or using Poetry
   poetry install
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   DB_CONNECTION_STRING=postgresql://username:password@localhost:5432/database_name
   ```

4. **Run the application**
   ```bash
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- **Interactive API docs**: `http://localhost:8000/docs`
- **ReDoc documentation**: `http://localhost:8000/redoc`

## API Endpoints

### POST /api/v1/identify

Identify and reconcile contact information.

**Request Body:**
```json
{
  "email": "user@example.com",
  "phoneNumber": "1234567890"
}
```

**Response:**
```json
{
  "contact": {
    "primaryContactId": 1,
    "emails": ["user@example.com", "user2@example.com"],
    "phoneNumbers": ["1234567890", "0987654321"],
    "secondaryContactIds": [2, 3]
  }
}
```

## Database Schema

### Contacts Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| email | String | Contact email address |
| phone_number | String | Contact phone number |
| linked_id | Integer | ID of the primary contact (for secondary contacts) |
| link_precedence | String | 'primary' or 'secondary' |
| created_at | DateTime | Contact creation timestamp |
| updated_at | DateTime | Last update timestamp |
| deleted_at | DateTime | Soft delete timestamp |

## Business Logic

### Contact Linking Rules

1. **Primary Contact**: The first contact created in a network becomes the primary contact
2. **Secondary Contacts**: Additional contacts in the same network become secondary contacts
3. **Automatic Linking**: When a new contact shares email or phone with existing contacts, they are automatically linked
4. **Network Expansion**: When multiple primary contacts are found, the oldest becomes primary and others become secondary
5. **Consistent Response**: The API always returns the same network information regardless of which contact's email/phone is used in the request

### Example Scenarios

1. **New Contact**: Creates a new primary contact
2. **Existing Contact**: Returns the existing contact network
3. **Linked Contacts**: Automatically links contacts and returns the complete network
4. **Multiple Primary Contacts**: Merges networks by making the oldest contact primary

## Development

### Running Tests
```bash
# Add test commands here when tests are implemented
```

### Code Style
This project follows PEP 8 style guidelines.

### Database Migrations
Currently using SQLAlchemy's `create_all()` for table creation. Consider using Alembic for production migrations.

## Deployment

### Production Considerations

1. **Environment Variables**: Set proper production environment variables
2. **Database**: Use a production-grade database (PostgreSQL recommended)
3. **Security**: Configure CORS properly for production domains
4. **Logging**: Implement proper logging
5. **Monitoring**: Add health checks and monitoring

### Docker Deployment
```dockerfile
# Add Dockerfile when needed
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license here]

## Support

For support and questions, please contact [your contact information]. 
