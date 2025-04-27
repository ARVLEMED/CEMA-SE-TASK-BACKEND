Healthcare Management Backend
This is a Flask-based REST API backend for a healthcare management system. It provides functionality for user authentication, client management, consultation tracking, and program enrollment. The API is designed to support a frontend application for healthcare professionals to manage patients (clients), record consultations, and enroll clients in programs.
Table of Contents

Features
Technologies
Project Structure
Setup Instructions
API Endpoints
Authentication
Clients
Consultations
Programs


Testing
Contributing
License

Features

User Authentication: Register and log in users with JWT-based authentication.
Client Management: Create, read, update, and delete (CRUD) client records.
Consultation Tracking: Record and manage consultation details for clients, including vitals, diagnosis, and treatment plans.
Program Enrollment: Enroll clients in healthcare programs (e.g., TB Program, HIV Program).
Secure Endpoints: All API endpoints (except signup and login) require JWT authentication.

Technologies

Python 3.8+: Programming language.
Flask: Web framework for building the API.
Flask-RESTful: Extension for creating RESTful APIs.
Flask-JWT-Extended: Extension for JWT authentication.
Flask-SQLAlchemy: ORM for database management.
SQLite: Lightweight database (can be swapped for PostgreSQL or another database).
Pipenv: Dependency management and virtual environment tool.

Project Structure
healthcare-backend/
│
├── app.py                  # Main Flask application file
├── models.py               # Database models (User, Client, Consultation, Program, Enrollment)
├── auth_routes.py          # Routes for user authentication (signup, login, user details)
├── client_routes.py        # Routes for client management and program enrollment
├── consultation_routes.py  # Routes for consultation management
├── program_routes.py       # Routes for program management
├── app.db                  # SQLite database file (generated after setup)
├── Pipfile                 # Dependency file for Pipenv
├── Pipfile.lock            # Lock file for Pipenv dependencies
└── README.md               # Project documentation

Setup Instructions
Prerequisites

Python 3.8 or higher
Pipenv (install with pip install pipenv)

Installation

Clone the Repository:
git clone https://github.com/yourusername/healthcare-backend.git
cd healthcare-backend


Set Up Virtual Environment and Install Dependencies:
pipenv install


Activate the Virtual Environment:
pipenv shell


Initialize the Database:

The project uses SQLite by default. To initialize the database, run the Flask app:pipenv run python app.py


This will create app.db in the project directory. Stop the server after the database is created (Ctrl+C).


Run the Application:
pipenv run python app.py

The API will be available at http://localhost:5000.


Environment Variables
No environment variables are required for the default setup (SQLite database). If you switch to another database (e.g., PostgreSQL), set the DATABASE_URL environment variable in your environment or a .env file:
DATABASE_URL=postgresql://username:password@localhost:5432/healthcare_db

API Endpoints
All endpoints (except /api/signup and /api/login) require a JWT token in the Authorization header:
Authorization: Bearer <your-jwt-token>

Authentication

POST /api/signup

Register a new user.
Request Body:{
  "email": "test@example.com",
  "password": "password123"
}


Response (201):{
  "message": "User created successfully",
  "access_token": "<jwt-token>",
  "user": { "id": 1, "email": "test@example.com" }
}


Error (400): If email already exists.


POST /api/login

Log in an existing user.
Request Body:{
  "email": "test@example.com",
  "password": "password123"
}


Response (200):{
  "access_token": "<jwt-token>",
  "user": { "id": 1, "email": "test@example.com" }
}


Error (401): If credentials are invalid.


GET /api/user

Retrieve the authenticated user’s details.
Response (200):{ "id": 1, "email": "test@example.com" }


Error (401): If no token is provided.



Clients

GET /api/clients

Retrieve all clients, with optional filters.
Query Parameters:
status (optional): Filter by status (e.g., status=waiting).
search (optional): Filter by name (e.g., search=Alice).


Response (200):[
  { "id": 1, "name": "Alice Smith", "age": 30, "status": "Waiting", "consultations": [], "enrollments_data": [] }
]




GET /api/clients/

Retrieve a client by ID.
Response (200):{ "id": 1, "name": "Alice Smith", "age": 30, "status": "Waiting", "consultations": [], "enrollments_data": [] }


Error (404): If client not found.


POST /api/clients

Create a new client.
Request Body:{
  "name": "Alice Smith",
  "age": 30,
  "status": "Waiting"
}


Response (201):{ "id": 1, "name": "Alice Smith", "age": 30, "status": "Waiting", "consultations": [], "enrollments_data": [] }


Error (400): If required fields are missing.


PUT /api/clients/

Update an existing client.
Request Body:{
  "name": "Alice Johnson",
  "age": 31,
  "status": "Active"
}


Response (200):{ "id": 1, "name": "Alice Johnson", "age": 31, "status": "Active", "consultations": [], "enrollments_data": [] }


Error (404): If client not found.


DELETE /api/clients/

Delete a client.
Response (200):{ "message": "Client deleted successfully" }


Error (404): If client not found.


POST /api/clients//enroll

Enroll a client in a program.
Request Body:{
  "programId": 1
}


Response (201):{ "message": "Client enrolled successfully" }


Error (400): If programId is missing.
Error (500): If client or program not found (should be improved to return 404).



Consultations

GET /api/consultations

Retrieve all consultations, with optional filter by client.
Query Parameters:
client_id (optional): Filter by client ID (e.g., client_id=1).


Response (200):[
  {
    "id": 1,
    "client_id": 1,
    "vitals": "BP: 120/80",
    "allergies": "Peanuts",
    "symptoms": "Cough",
    "medical_history": "Hypertension",
    "medications": "Lisinopril",
    "diagnosis": "Flu",
    "investigations": "Chest X-ray",
    "treatment_plan": "Rest, fluids"
  }
]




GET /api/consultations/

Retrieve a consultation by ID.
Response (200):{
  "id": 1,
  "client_id": 1,
  "vitals": "BP: 120/80",
  "allergies": "Peanuts",
  "symptoms": "Cough",
  "medical_history": "Hypertension",
  "medications": "Lisinopril",
  "diagnosis": "Flu",
  "investigations": "Chest X-ray",
  "treatment_plan": "Rest, fluids"
}


Error (404): If consultation not found.


POST /api/consultations

Create a new consultation.
Request Body:{
  "client_id": 1,
  "vitals": "BP: 120/80",
  "allergies": "Peanuts",
  "symptoms": "Cough",
  "medical_history": "Hypertension",
  "medications": "Lisinopril",
  "diagnosis": "Flu",
  "investigations": "Chest X-ray",
  "treatment_plan": "Rest, fluids"
}


Response (201):{
  "id": 1,
  "client_id": 1,
  "vitals": "BP: 120/80",
  "allergies": "Peanuts",
  "symptoms": "Cough",
  "medical_history": "Hypertension",
  "medications": "Lisinopril",
  "diagnosis": "Flu",
  "investigations": "Chest X-ray",
  "treatment_plan": "Rest, fluids"
}


Error (400): If client_id is missing.
Error (404): If client not found.


PUT /api/consultations/

Update an existing consultation.
Request Body:{
  "client_id": 1,
  "vitals": "BP: 118/78",
  "allergies": "Peanuts",
  "symptoms": "Cough, Fever",
  "medical_history": "Hypertension",
  "medications": "Lisinopril",
  "diagnosis": "Flu",
  "investigations": "Chest X-ray, Blood Test",
  "treatment_plan": "Antibiotics, Rest"
}


Response (200):{
  "id": 1,
  "client_id": 1,
  "vitals": "BP: 118/78",
  "allergies": "Peanuts",
  "symptoms": "Cough, Fever",
  "medical_history": "Hypertension",
  "medications": "Lisinopril",
  "diagnosis": "Flu",
  "investigations": "Chest X-ray, Blood Test",
  "treatment_plan": "Antibiotics, Rest"
}


Error (404): If consultation or client not found.


DELETE /api/consultations/

Delete a consultation.
Response (200):{ "message": "Consultation deleted successfully" }


Error (404): If consultation not found.



Programs

GET /api/programs

Retrieve all programs.
Response (200):[
  { "id": 1, "name": "TB Program" },
  { "id": 2, "name": "HIV Program" }
]




GET /api/programs/

Retrieve a program by ID.
Response (200):{ "id": 1, "name": "TB Program" }


Error (404): If program not found.


POST /api/programs

Create a new program.
Request Body:{
  "name": "TB Program"
}


Response (201):{ "id": 1, "name": "TB Program" }


Error (400): If name is missing.


PUT /api/programs/

Update an existing program.
Request Body:{
  "name": "Updated TB Program"
}


Response (200):{ "id": 1, "name": "Updated TB Program" }


Error (404): If program not found.


DELETE /api/programs/

Delete a program.
Response (200):{ "message": "Program deleted successfully" }


Error (404): If program not found.



Contributing

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Make your changes and commit (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
