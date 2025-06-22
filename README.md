# Bitespeed Identity Reconciliation Service

A FastAPI-based service for identifying and reconciling customer contact information across multiple orders.

## Features

- Identify and link customer contacts based on email and phone number
- Maintain primary and secondary contact relationships
- RESTful API endpoint for contact identification
- PostgreSQL database integration
- Containerized with Docker

## Prerequisites

- Python 3.8+
- PostgreSQL database
- Docker (optional)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Identity-Reconciliation
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

4. Set up environment variables:
   Create a `.env` file in the project root with the following content:
   ```
   DB_CONNECTION_STRING=postgresql://username:password@localhost:5432/dbname
   ```

## Running the Application

### Development

1. Start the FastAPI development server:
   ```bash
   uvicorn main:app --reload
   ```

2. The API will be available at `http://localhost:8000`

### Production with Docker

1. Build the Docker image:
   ```bash
   docker build -t identity-reconciliation .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 --env-file .env identity-reconciliation
   ```

## API Documentation

Once the application is running, you can access:

- API Documentation: `http://localhost:8000/docs`
- Alternative Documentation: `http://localhost:8000/redoc`

## API Endpoint

### Identify Contact

- **URL**: `/identify`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "email": "example@example.com",
    "phoneNumber": "1234567890"
  }
  ```
  Note: At least one of `email` or `phoneNumber` is required.

- **Success Response**:
  - **Code**: 200
  - **Content**:
    ```json
    {
      "contact": {
        "primaryContactId": 1,
        "emails": ["example@example.com"],
        "phoneNumbers": ["1234567890"],
        "secondaryContactIds": []
      }
    }
    ```

## Database Schema

The service uses the following database schema:

```sql
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(20),
    email VARCHAR(255),
    linked_id INTEGER REFERENCES contacts(id),
    link_precedence VARCHAR(10) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP
);

-- Indexes for better query performance
CREATE INDEX idx_contacts_email ON contacts(email);
CREATE INDEX idx_contacts_phone_number ON contacts(phone_number);
CREATE INDEX idx_contacts_linked_id ON contacts(linked_id);
```

## Testing

To run the tests:

```bash
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 
