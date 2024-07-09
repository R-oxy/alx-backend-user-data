```markdown
# 0x01. Basic Authentication

## Background Context

This project explores the implementation of Basic Authentication on a simple API using Python and Flask. Basic Authentication involves encoding user credentials in the HTTP headers, which is a fundamental mechanism often used for learning purposes but not recommended for production without proper security considerations.

## Resources

To effectively complete this project, familiarize yourself with:

- REST API Authentication Mechanisms
- Base64 encoding in Python
- HTTP header Authorization
- Flask framework basics

## Learning Objectives

By the end of this project, you should be able to:

- Explain what authentication means in the context of web APIs
- Understand Base64 encoding and its usage in HTTP headers
- Implement Basic Authentication from scratch using Python and Flask
- Secure API endpoints by validating user credentials passed via headers

## Requirements

### Python Scripts

- All scripts should be compatible with Python 3.7 on Ubuntu 18.04 LTS.
- Follow PEP8 coding style guidelines (`pycodestyle` version 2.5).
- Include necessary shebang (`#!/usr/bin/env python3`) at the start of each script.
- Ensure all scripts are executable and end with a newline.
- Provide comprehensive documentation for all modules, classes, and functions.

## Tasks Overview

### 1. Error handler: Unauthorized

Implement an error handler to respond with a 401 status code for unauthorized requests.

### 2. Error handler: Forbidden

Create an error handler for requests where the user is authenticated but not authorized to access a resource (403 status code).

### 3. Auth class

Define a base `Auth` class with placeholder methods for managing API authentication.

### 4. Define which routes don't need authentication

Update the `require_auth` method in `Auth` to specify routes that don't require authentication.

### 5. Request validation!

Implement request validation to secure the API, using Flask's `before_request` method.

### 6. Basic auth

Extend the `Auth` class with a `BasicAuth` subclass for Basic Authentication.

### 7. Basic - Base64 part

Implement methods in `BasicAuth` to extract and decode the Base64 part of the Authorization header.

### 8. Basic - Base64 decode

Add functionality to decode the Base64 Authorization header in `BasicAuth`.

### 9. Basic - User credentials

Implement methods to extract user credentials from the decoded Base64 Authorization header.

### 10. Basic - User object

Create a method to retrieve a `User` object based on provided credentials in `BasicAuth`.

### 11. Basic - Overload current_user - and BOOM!

Finalize Basic Authentication by overriding the `current_user` method to validate user credentials and retrieve the associated `User` object.

## Files

The project structure should include:

- `api/v1/app.py`: Main Flask application file.
- `api/v1/views/index.py`: Contains API endpoints.
- `api/v1/auth/`: Directory for authentication related files.
- `models/`: Directory for user data model (`User`).

## Setup and Initialization

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your_username/alx-backend-user-data.git
   cd 0x01-Basic_authentication
   ```

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Run the Flask application:**
   ```bash
   API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
   ```

## Routes

- `/api/v1/status`: GET - Check API status.
- `/api/v1/unauthorized`: GET - Endpoint to trigger a 401 error.
- `/api/v1/forbidden`: GET - Endpoint to trigger a 403 error.
- Additional routes as per the implementation of Basic Authentication.
