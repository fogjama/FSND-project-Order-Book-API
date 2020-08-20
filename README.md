# Full Stack Capstone Project

## Getting Started

### Run Locally

#### Installing Dependencies

A virtual environment is recommended for running the application. 

Once you have your virtual environment set up and running, install dependencies from the `requirements.txt` file:

```pip install -r requirements.txt

```

This will install all of the required packages.

#### Database Setup

To create the database structure in your local postgres database, run the following commands:

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

#### Environment Variables

The following environment variables must be set:
* DATABASE_URL : full path to SQL database. Example: `postgres://{user}:{password}@{path}/{database_name}`
* AUTH0_DOMAIN : domain for Auth0 account. Example: `{user}.eu.auth0.com`
* API_AUDIENCE : value from Auth0 API definition

### Deploy to Heroku

#### Install Dependencies

#### Database Setup


## API Documentation

### Endpoints

#### GET '/customers?page={page}

- Fetches a paginated list of customers with 10 items per page. 
- Request arguments: Optional page argument of type integer (default to 1 if absent)
- Returns 

Example:
```
curl -X GET http://localhost:5000/customers?page=2
```
Response:
```

```

#### GET '/orders?page={page}

#### GET '/deliveries?page={page}

#### GET '/customers/{customer_id}

#### GET '/orders/{order_id}

#### GET '/deliveries/{delivery_id}

#### GET '/customers/{customer_id}/orders'

#### GET '/orders/{order_id}/deliveries'

#### POST '/customers'

#### POST '/orders'

#### POST '/deliveries'

#### PATCH '/customers/{customer_id}

#### PATCH '/orders/{order_id}

#### DELETE '/orders/{order_id}

#### DELETE '/deliveries/{delivery_id}