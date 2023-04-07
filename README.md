# Web Portal for Voting System
### This repository contains the source code for an API that services a web application called Votify, a website for shared polls. You can visit the website through [This Link](https://polls-app-alaaamady.vercel.app)

## Prerequisites

Before you can start using Git and Python, you need to make sure you have the following software installed on your computer:

- Git: Git is a version control system that allows you to track changes to your code over time. To install Git, follow the instructions for your operating system at https://git-scm.com/downloads.

- Pip: Pip is a package manager for Python that allows you to easily install and manage third-party libraries and modules. To install Pip, follow the instructions at https://pip.pypa.io/en/stable/installation/.

- Python: Python is a popular programming language used for a wide range of applications, including web development, data analysis, and machine learning. To install Python, follow the instructions for your operating system at https://www.python.org/downloads/.
## Installation

## API
To run the Django REST API, follow these steps:

1. Clone the repository onto your local machine using the following command:

`git clone https://github.com/alaaamady/polls-api.git`

2. Navigate to the project's root directory and create a virtual environment:

`python -m venv venv`

3. Activate the virtual environment:

`source venv/bin/activate`

4. Install the required packages:

`pip install -r requirements.txt`

5. Configure the postgres database by setting up a local database or a hosted one and then set up the following environment variables in your root project `.env` file:

```
## .env file

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

6. Run database migration: 

`python manage.py migrate`


7. Setup the sender email host and password by adding the following varialvles to you `.env` file

```
EMAIL_ADDRESS=
EMAIL_PASSWORD=
``````
57

6. Start the server:
`python manage.py runserver`

## Endpoints list
|Name|  Description |
|--|--|
| /GET /polls?page= | Lists all polls in a paginated response of maximum 10 entries |
| /GET /polls?search= | Searches all polls' titles, description or choices |
| /POST /vote | Submits a vote for verification |
| /POST /confirm-vote | Verifies a vote's OTP|




## To be improved

1. The current implementation only has unit tests for the views module. it should cover all app modules, eg. Serializers, Models.
2. An OpenAPI documentation would aid in on boarding users to utilize this API quicker. for now there is a Postmand collection for all endpoints.
3.  Use a secure method for generating and storing the OTP, such as using a cryptographically secure random number generator and storing the OTP in hashed form.
4.  Implement rate limiting and/or CAPTCHA to prevent automated attacks that attempt to guess OTPs.
5.  Log all OTP generation, sending, and validation activities, to allow for audit trails and investigation in case of suspicious activities.
