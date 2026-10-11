# Smart Placement Management System

A Django-based web application designed to manage the complete campus placement process for students and administrators.

## Features

### Student
- Student registration and login
- Profile and academic details management
- Resume upload
- View eligible job drives
- Apply to jobs
- Track application status
- View scheduled interviews
- Receive placement notifications
- View placement statistics

### Admin / TPO
- Admin dashboard with placement statistics
- Create and manage job drives
- Configure custom application form fields
- Review student applications
- Shortlist or reject candidates
- Schedule interviews
- Mark students as selected
- Track placement progress

## Tech Stack

- Python
- Django
- SQLite
- HTML
- CSS
- Bootstrap
- JavaScript
- Git
- GitHub

## Project Structure

- accounts - authentication and user roles
- students - student profile management
- companies - company information
- jobs - job drives and eligibility
- applications - job application workflow
- interviews - interview scheduling
- notifications - student notifications
- placements - placement-related functionality
- dashboard - student and admin dashboards

## Installation

Clone the repository:

`ash
git clone https://github.com/rsah123/smart-placement-management-system.git
cd smart-placement-management-system
`

Create a virtual environment:

`ash
python -m venv venv
`

Activate it on Windows:

`ash
venv\Scripts\activate
`

Install dependencies:

`ash
pip install -r requirements.txt
`

Create a .env file using .env.example as reference.

Run migrations:

`ash
python manage.py migrate
`

Create an admin user:

`ash
python manage.py createsuperuser
`

Start the development server:

`ash
python manage.py runserver
`

Open:

`	ext
http://127.0.0.1:8000/
`

## Security

Sensitive configuration such as the Django secret key is stored using environment variables and is not committed to GitHub.

## Future Improvements

- Recruiter-specific workflow
- Email notifications
- Advanced placement analytics
- PostgreSQL support
- Cloud deployment
- REST API integration

## Author

Ranjan Kumar
