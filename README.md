# Authentication 
 
# Role-Based Authentication API

## Overview

This API allows users to register, login, and manage roles such as mentor, companion, and HR. The system uses Django and Django REST Framework for backend functionality and authentication.

## Installation

### Prerequisites

- Python 3.6+
- pip (Python package installer)

### Steps

1. **Clone the repository**:
    ```sh
    git clone https://github.com/ayshathlubabaka/Authentication
    cd your-repository
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv aenv
    source aenv/bin/activate    # On Windows use `aenv\Scripts\activate`
    ```

3. **Install the requirements**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Run database migrations**:
    ```sh
    python manage.py migrate
    ```

5. **Create groups and permissions**:
    ```sh
    python manage.py create_groups_and_permissions
    ```

6. **Run the development server**:
    ```sh
    python manage.py runserver
    ```

## Register a New User

To register a new user, make a `POST` request to:


### Example JSON Data for Registration

```json
{
    "firstname": "John",
    "lastname": "Doe",
    "email": "john.doe@example.com",
    "password": "securepassword123",
    "roles": ["mentor", "companion"]
}

{
    "email": "john.doe@example.com",
    "password": "securepassword123",
    "role": "mentor"
}

// .env

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.your_email_host.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password