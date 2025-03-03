# Loan Management System - Django REST API

## Overview
The Loan Management System is a Django-based REST API for managing loans with monthly compound interest. It supports role-based authentication, automatic EMI calculations, and loan foreclosure.

## Features
- User authentication with JWT  
- Loan application & approval process  
- Automatic interest & EMI calculations  
- Loan foreclosure with adjusted interest  
- Secure API with role-based access control  

## Tech Stack
- **Backend:** Django, Django REST Framework  
- **Authentication:** JWT
- **Database:** PostgreSQL  
- **Deployment:** Render  

---


## Installation

# Clone the repository
git clone "https://github.com/Gowri-nandhana/Loan_management_system.git"
cd loanmanagement

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser 
python manage.py createsuperuser

# Run the server
python manage.py runserver


---

##  API ENDPOINTS

## Authentication

# User registration
POST /api/register/

# login
POST /api/login/

# logout
POST /api/logout/

# Admin login
POST /api/login/

## Loans

# Adding loans
POST /api/loans/add/

# Viewing loans
GET /api/loans/

# Foreclose a Loan
POST /api/loans/{loan_id}/foreclose/

# View Loans (Admin Only)
POST /api/loans/all/
---

# contact
email : gowri.nandhana.2909@gmail.com




