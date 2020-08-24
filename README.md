# Full Stack Capstone Project

## Getting Started

### Run Locally

#### Installing Dependencies

A virtual environment is recommended for running the application. 

Once you have your virtual environment set up and running, install dependencies from the `requirements.txt` file:

```
pip install -r requirements.txt
```

This will install all of the required packages.

#### Database Setup

Create a local postgres database called *orders_application* 

To create the database structure in your local postgres database, run the following commands:

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

*NOTE: Modify the environment variable DATABASE_URL in the file **setup.sh** to reflect your local postgres database settings, before running `source setup.sh` to set environment variables for testing*

#### Environment Variables

The following environment variables must be set:
- DATABASE_URL : full path to SQL database. Example: `postgres://{user}:{password}@{path}/{database_name}`
- AUTH0_DOMAIN : domain for Auth0 account. Example: `{user}.eu.auth0.com`
- API_AUDIENCE : value from Auth0 API definition
- CLIENT_ID : Client ID of Auth0 application (used for login URL).
- APP_URL : Local or public URL of running application (used for redirect after login). Example `http://localhost:8080/`

For testing purposes using **test_app.py**:
- ADMIN_TOKEN : valid token for Admin role
- USER_TOKEN : valid token for User role

To set these environment variables using default values saved in the **setup.sh** file, run `source setup.sh`

### Deploy to Heroku

#### Create and Set Up Heroku App

1. To create the Heroku app, run `heroku create {name_of_app}`.
2. Using the git URL returned from step 1, run `git remote add heroku {heroku_git_url}`
3. To set up postgresql add-on for the app database, run `heroku addons:create heroku-postgresql:hobby-dev --app {name_of_app}` (or subsitute `hobby-dev` if you are running on a paid tier)
4. Log in to Heroku and set the environment variables AUTH0_DOMAIN and API_AUDIENCE (see above for definitions)
5. Push files from local git repo by running `git push heroku master`
6. Run database migrations by running `heroku run python manage.py db upgrade --app {name_of_app}`

## Authorization

### Identity Provider

Auth0 is used as an identity provider.

### Roles

Available user roles are:
- Administrator: Administrators can create, read, update, and delete records
- User: Users can read records but cannot create, update, or delete

### Login / Acquiring a Token

To acquire a JWT token, visit the endpoint `/login`. This redirects to the Auth0 login page for the application. After successful login, redirects back to the `/login-result` endpoint with instruction to copy the token from the address bar for use in API calls.

Note that while a user can be registered using the `/login` endpoint, no resources can be accessed until the user is granted permissions in Auth0.

## API Documentation

### Endpoints

#### GET '/'

- Default application endpoint.
- Returns success and URL to GitHub repo

Response:
```
{
  "message": "Documentation avaialble on GitHub at https://github.com/fogjama/FSND-capstone", 
  "success": true
}
```

#### GET '/orders?page={page}

- Fetches a paginated list of orders with 10 items per page. 
- Request arguments: Optional page argument of type integer (default to 1 if absent)
- Returns list of dictionaries and total number of orders
- Required access: `read:orders`

Sample request:
```
curl -X GET https://fsnd-order-book-jaf9481.herokuapp.com/orders?page=1 -H "Authorization: Bearer $TOKEN"
```
Sample response:
```
{
  "orders": [
    {
      "customer": 1,
      "date": "Sat, 25 Jul 2020 00:00:00 GMT",
      "id": 1,
      "value": 99.99
    },
    {
      "customer": 1,
      "date": "Sun, 26 Jul 2020 00:00:00 GMT",
      "id": 2,
      "value": 101.2
    },
    {
      "customer": 1,
      "date": "Fri, 31 Jul 2020 00:00:00 GMT",
      "id": 4,
      "value": 15.43
    },
    {
      "customer": 1,
      "date": "Fri, 21 Aug 2020 22:27:35 GMT",
      "id": 5,
      "value": 22.5
    },
    {
      "customer": 1,
      "date": "Sun, 23 Aug 2020 16:52:05 GMT",
      "id": 6,
      "value": 22.5
    },
    {
      "customer": 1,
      "date": "Sun, 23 Aug 2020 17:49:35 GMT",
      "id": 7,
      "value": 22.5
    },
    {
      "customer": 1,
      "date": "Sun, 23 Aug 2020 17:52:49 GMT",
      "id": 8,
      "value": 22.5
    }
  ],
  "success": true,
  "total_orders": 7
}
```

#### GET '/customers?page={page}

- Fetches a paginated list of customers with 10 items per page
- Request arguments: Optional page argument of type integer (default to 1 if absent)
- Returns customers as list of dictionaries and total number of customers
- Required access: `read:customers`

Sample request:
```
curl -X GET https://fsnd-order-book-jaf9481.herokuapp.com/customers?page=1 -H "Authorization: Bearer $TOKEN"
```
Sample response:
```
{
  "customers": [
    {
      "active": true,
      "id": 2,
      "name": "Ella Forcraft"
    },
    {
      "active": true,
      "id": 3,
      "name": "John Major"
    },
    {
      "active": true,
      "id": 4,
      "name": "John Smith"
    },
    {
      "active": true,
      "id": 5,
      "name": "John Smith"
    },
    {
      "active": true,
      "id": 6,
      "name": "John Smith"
    },
    {
      "active": true,
      "id": 1,
      "name": "Walla Wanga"
    }
  ],
  "success": true,
  "total_customers": 6
}
```

#### GET '/deliveries?page={page}

- Fetches a paginated list of deliveries with 10 items per page
- Request arguments: Optional page argument of type integer (defaults to 1 if omitted)
- Returns deliveries as a list of dictionaries and total number of deliveries 
- Required access: `read:deliveries`

Sample request:
```
curl -X GET https://fsnd-order-book-jaf9481.herokuapp.com/deliveries?page=1 -H "Authorization: Bearer $TOKEN"
```
Sample response:
```
{
  "deliveries": [
    {
      "delivery_date": "Sat, 01 Aug 2020 00:00:00 GMT",
      "id": 1,
      "order": 1
    },
    {
      "delivery_date": "Tue, 04 Aug 2020 00:00:00 GMT",
      "id": 2,
      "order": 2
    },
    {
      "delivery_date": "Mon, 10 Aug 2020 00:00:00 GMT",
      "id": 4,
      "order": 3
    },
    {
      "delivery_date": "Fri, 21 Aug 2020 22:27:39 GMT",
      "id": 5,
      "order": 1
    },
    {
      "delivery_date": "Sun, 23 Aug 2020 17:49:40 GMT",
      "id": 6,
      "order": 1
    },
    {
      "delivery_date": "Sun, 23 Aug 2020 17:52:54 GMT",
      "id": 7,
      "order": 1
    }
  ],
  "success": true,
  "total_deliveries": 6
}
```

#### GET '/customers/{customer_id}

- Fetches a single customer by its id
- Returns the selected customer as a dictionary object, or 404
- Required access: `read:customers`

Sample request:
```
curl -X GET https://fsnd-order-book-jaf9481.herokuapp.com/customers/2 -H "Authorization: Bearer $TOKEN"
```
Sample response:
```
{
  "customer": {
    "active": true,
    "id": 2,
    "name": "Ella Forcraft"
  },
  "success": true
}
```

#### GET '/orders/{order_id}

- Fetches a single order by its id
- Returns the selected order as a dictionary object, or 404
- Required access: `read:orders`

Sample request:
```
curl -X GET https://fsnd-order-book-jaf9481.herokuapp.com/orders/5 -H "Authorization: Bearer $TOKEN"
```
Sample response:
```
{
  "order": {
    "customer": 1,
    "date": "Fri, 21 Aug 2020 22:27:35 GMT",
    "id": 5,
    "value": 22.5
  },
  "success": true
}
```
#### GET '/deliveries/{delivery_id}

- Fetches a single delivery by its id
- Returns the selected delivery as a dictionary object, or 404
- Required access: `read:deliveries`

Sample request:
```
curl -X GET https://fsnd-order-book-jaf9481.herokuapp.com/deliveries/5 -H "Authorization: Bearer $TOKEN"
```
Sample response:
```
{
  "delivery": {
    "delivery_date": "Fri, 21 Aug 2020 22:27:39 GMT",
    "id": 5,
    "order": 1
  },
  "success": true
}
```

#### GET '/customers/{customer_id}/orders?page={page}'

- Fetches paginated list of orders linked to specific customer ID, with 10 items per page
- Request arguments: Optional page argument as integer (defaults to 1 if omitted)
- Returns list of dictionaries and total number of orders for customer
- Required access: `read:orders`

Sample request:
```
curl -X GET https://fsnd-order-book-jaf9481.herokuapp.com/customers/1/orders?page=1 -H "Authorization: Bearer $TOKEN"
```
Sample response:
```
{
  "orders": [
    {
      "customer": 1,
      "date": "Sat, 25 Jul 2020 00:00:00 GMT",
      "id": 1,
      "value": 99.99
    },
    {
      "customer": 1,
      "date": "Sun, 26 Jul 2020 00:00:00 GMT",
      "id": 2,
      "value": 101.2
    },
    {
      "customer": 1,
      "date": "Fri, 31 Jul 2020 00:00:00 GMT",
      "id": 4,
      "value": 15.43
    },
    {
      "customer": 1,
      "date": "Fri, 21 Aug 2020 22:27:35 GMT",
      "id": 5,
      "value": 22.5
    },
    {
      "customer": 1,
      "date": "Sun, 23 Aug 2020 16:52:05 GMT",
      "id": 6,
      "value": 22.5
    },
    {
      "customer": 1,
      "date": "Sun, 23 Aug 2020 17:49:35 GMT",
      "id": 7,
      "value": 22.5
    },
    {
      "customer": 1,
      "date": "Sun, 23 Aug 2020 17:52:49 GMT",
      "id": 8,
      "value": 22.5
    }
  ],
  "success": true,
  "total_orders": 7
}
```

#### GET '/orders/{order_id}/deliveries'

- Fetches list of all deliveries linked to specific order id
- Returns deliveries as list of dictionaries and total number of deliveries
- Required access: `read:deliveries`

Sample request:
```
curl -X https://fsnd-order-book-jaf9481.herokuapp.com/orders/1/deliveries -H "Authorization: Bearer $TOKEN"
```
Sample response:
```
{
  "deliveries": [
    {
      "delivery_date": "Sat, 01 Aug 2020 00:00:00 GMT",
      "id": 1,
      "order": 1
    },
    {
      "delivery_date": "Fri, 21 Aug 2020 22:27:39 GMT",
      "id": 5,
      "order": 1
    },
    {
      "delivery_date": "Sun, 23 Aug 2020 17:49:40 GMT",
      "id": 6,
      "order": 1
    },
    {
      "delivery_date": "Sun, 23 Aug 2020 17:52:54 GMT",
      "id": 7,
      "order": 1
    }
  ],
  "success": true,
  "total_deliveries": 4
}
```

#### POST '/customers'

- Creates a new customer
- Returns the added customer with its ID
- Required access: `post:customers`

Sample request:
```
curl --request POST 'https://fsnd-order-book-jaf9481.herokuapp.com/customers' \
--header 'Authorization: Bearer $TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "John Smith",
    "active": true
}'
```
Sample response:
```
{
  "customer": {
    "active": true,
    "id": 10,
    "name": "John Smith"
  },
  "success": true
}
```

#### POST '/orders'

- Creates a new order
- Returns the created order with its ID
- Requred access: `post:orders`

Sample request:
```
curl --request POST 'https://fsnd-order-book-jaf9481.herokuapp.com/orders' \
--header 'Authorization: Bearer $TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{
    "customer": 10,
    "value": 99.98,
    "date": "2020-08-19"
}'
```
Sample response:
```
{
  "order": {
    "customer": 10,
    "date": "Wed, 19 Aug 2020 00:00:00 GMT",
    "id": 9,
    "value": 99.98
  },
  "success": true
}
```

#### POST '/deliveries'

- Creates new delivery
- Returns created delivery with its ID
- Required access: `post:deliveries`

Sample request:
```
curl --request POST 'https://fsnd-order-book-jaf9481.herokuapp.com/deliveries' \
--header 'Authorization: Bearer $TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{
    "order": 9,
    "delivery_date": "2020-08-23"
}'
```
Sample response:
```
{
  "delivery": {
    "delivery_date": "Sun, 23 Aug 2020 00:00:00 GMT",
    "id": 8,
    "order": 9
  },
  "success": true
}
```

#### PATCH '/customers/{customer_id}

- Updates customer record by ID
- Returns ID of updated record
- Required access: `update:customers`

Sample request:
```
curl --request PATCH 'https://fsnd-order-book-jaf9481.herokuapp.com/customers/10' \
--header 'Authorization: Bearer $TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{
    "active": true
}'
```
Sample response:
```
{
  "id": 10,
  "success": true
}
```

#### PATCH '/orders/{order_id}

- Updates order record by ID
- Returns ID of updated record
- Required access: `update:orders`

Sample request:
```
curl --request PATCH 'https://fsnd-order-book-jaf9481.herokuapp.com/orders/5' \
--header 'Authorization: Bearer $TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{
    "value": 105.20
}'
```
Sample response:
```
{
    "id": 5,
    "success": true
}
```

#### DELETE '/orders/{order_id}

- Deletes order record by ID
- Returns ID of deleted record
- Required access: `delete:orders`

Sample request:
```
curl --request DELETE 'https://fsnd-order-book-jaf9481.herokuapp.com/orders/5' \
--header 'Authorization: Bearer $TOKEN'
```
Sample response:
```
{
    "deleted": "5",
    "success": true
}
```

#### DELETE '/deliveries/{delivery_id}

- Deletes delivery record by ID
- Returns ID of deleted record
- Required access: `delete:deliveries`

Sample request:
```
curl --request DELETE 'https://fsnd-order-book-jaf9481.herokuapp.com/deliveries/9' \
--header 'Authorization: Bearer $TOKEN'
```
Sample response:
```
{
    "deleted": "9",
    "success": true
}
```
