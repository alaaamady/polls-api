# Web Portal for Voting System
### This repository contains the source code for a web portal that provides access to a voting system's various features. The website can be accessed at [This Link](https://polls-app-alaaamady.vercel.app)

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

## Endpoints list
|Name|  Description |
|--|--|
| /GET /polls | Lists all polls in a paginated response of maximum 10 entries |
| /GET /polls?search= |searches all polls' titles, description or choices |
| /POST /vote |submits a vote for verification |
| /POST /confirm-vote |verifies a vote's OTP|




## To be imporovised

1. The current implementation only has unit tests for the views module. it should cover all app modules, eg. Serializers, Models.
2. an OpenAPI documentation would aid in on boarding users to utilize this API quicker. for now there is a Postmand collection for all endpoints.
3.  Use a secure method for generating and storing the OTP, such as using a cryptographically secure random number generator and storing the OTP in hashed form.
4.  Implement rate limiting and/or CAPTCHA to prevent automated attacks that attempt to guess OTPs.
5.  Log all OTP generation, sending, and validation activities, to allow for audit trails and investigation in case of suspicious activities.
