# BailReckoner

BailReckoner is a comprehensive bail application management system designed to streamline the bail application process for lawyers, judges, and viewers. The platform facilitates the creation, submission, review, and tracking of bail applications in a secure and organized manner.

## Features

### For Lawyers
- Create and manage bail applications
- Upload necessary documents (bail application forms, FIR copies, etc.)
- Track application status
- Submit applications for review

### For Judges
- Review submitted bail applications
- Make decisions (approve/reject)
- Set bail amounts
- View decision history

### For Viewers
- Search for bail applications by case number
- View application status and details
- Track bail application progress

## Security Features
- Role-based access control
- Case number required for viewers to access application information
- Secure document handling

## Installation and Setup

1. Clone the repository:
```
git clone https://github.com/aaryxnblondead/bailbail.git
cd bailbail
```

2. Create a virtual environment and install dependencies:
```
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
```

3. Run migrations:
```
python manage.py migrate
```

4. Create a superuser:
```
python manage.py createsuperuser
```

5. Run the development server:
```
python manage.py runserver
```

6. Access the application at http://127.0.0.1:8000/

## Tech Stack
- Django 5.0.4
- Bootstrap 4
- SQLite (development) / PostgreSQL (production-ready)
- HTML, CSS, JavaScript

## License
This project is licensed under the MIT License - see the LICENSE file for details. 