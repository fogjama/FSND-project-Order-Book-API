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

## Authorization

### Identity Provider

Auth0 is used as an identity provider.

### Roles

Available user roles are:
- Administrator: Administrators can create, read, update, and delete records
- User: Users can read records but cannot create, update, or delete

## API Documentation

### Endpoints

#### GET '/orders?page={page}

- Fetches a paginated list of orders with 10 items per page. 
- Request arguments: Optional page argument of type integer (default to 1 if absent)
- Returns list of dictionaries and total number of orders

Sample request:
```
curl -X GET http://localhost:5000/orders?page=1 -H "Authorization: Bearer $TOKEN"
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

Sample request:
```
curl -X GET http://localhost:8080/customers?page=1 -H "Authorization: Bearer $TOKEN"
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

Sample request:
```
curl -X GET http://localhost:8080/deliveries?page=1 -H "Authorization: Bearer $TOKEN"
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

Sample request:
```
curl -X GET http://localhost:8080/customers/2 -H "Authorization: Bearer $TOKEN"
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

Sample request:
```
curl -X GET http://localhost:8080/orders/5 -H "Authorization: Bearer $TOKEN"
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

Sample request:
```
curl -X GET http://localhost:8080/deliveries/5 -H "Authorization: Bearer $TOKEN"
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

Sample request:
```
curl -X GET http://localhost:8080/customers/1/orders?page=1 -H "Authorization: Bearer $TOKEN"
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

Sample request:
```
curl -X http://localhost:8080/orders/1/deliveries -H "Authorization: Bearer $TOKEN"
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

#### POST '/orders'

#### POST '/deliveries'

#### PATCH '/customers/{customer_id}

#### PATCH '/orders/{order_id}

#### DELETE '/orders/{order_id}

#### DELETE '/deliveries/{delivery_id}