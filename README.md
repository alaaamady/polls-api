# Web Portal for Voting System
## This repository contains the source code for a web portal that provides access to a voting system's various features. The website can be accessed at (this link)[https://polls-app-alaaamady.vercel.app/]

### Installation

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

5. Set up the database:

```
## .env file

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
EMAIL_ADDRESS=
EMAIL_PASSWORD=
```
`python manage.py migrate`


6. Start the server:
`python manage.py runserver`
