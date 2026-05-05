# Security Sandbox Setup Guide

This guide covers the entire process of setting up, configuring, and launching the Security Educational Django App from scratch.

## Prerequisites
Ensure you have Python 3 installed on your system.

## 1. Environment Setup

First, create a virtual environment to isolate the project dependencies:
```bash
python -m venv venv
```

Activate the virtual environment:
- **On Linux/macOS:**
  ```bash
  source venv/bin/activate
  ```
- **On Windows:**
  ```bash
  venv\Scripts\activate
  ```

## 2. Install Dependencies

With your virtual environment active, install the required packages (Django, sqlparse, etc.) from the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

## 3. Database Initialization

The project uses SQLite by default. Run the following commands to create the database tables:
```bash
python manage.py makemigrations
python manage.py migrate
```

## 4. Seeding the Database

To interact with the SQL Injection sandbox, you need data. A custom management command has been created to automatically populate the database using the `seed_data.json` file.

Run the following command to seed both the `Employee` and `Subscriber` tables with mock data:
```bash
python manage.py seed_db
```
*You should see output confirming that 10 employees and 10 subscribers were successfully seeded.*

## 5. Launch the Application

Start the Django development server:
```bash
python manage.py runserver
```

Open your web browser and navigate to:
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Additional Resources
- **`sqlreadme.md`**: Explains the difference between vulnerable, safe, and raw SQL query execution modes.
- **`seed_data.json`**: Contains the raw JSON data injected into the SQLite database during the seed process.
