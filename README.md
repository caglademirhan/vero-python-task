# Vero Digital Python Task

This project consists of a client-side script (`try_cli.py`) and a server-side script (`try.py`) that together achieve the following tasks:

## Task Description

### Client Side

The client-side script is responsible for transmitting a CSV file to a REST API, handling the response, and generating an Excel file based on specified input parameters.

#### Input Parameters

- `-k/--keys`: A parameter that can receive an arbitrary number of string arguments.
- `-c/--colored`: A boolean flag that defaults to True.

#### Steps

1. Transmit the CSV file containing vehicle information to the server.
2. Convert the server's response into an Excel file with the following criteria:
   - Rows are sorted by the `gruppe` field.
   - Columns always contain the `rnr` field.
   - Only keys that match the input arguments are considered as additional columns.
   - If `labelIds` are given and at least one colorCode could be resolved, use the first colorCode to tint the cell's text.
   - If the `-c` flag is True, color each row based on the following logic:
     - If `hu` is not older than 3 months, color the row green (#007500).
     - If `hu` is not older than 12 months, color the row orange (#FFA500).
     - If `hu` is older than 12 months, color the row red (#b30000).
   - The file should be named `vehicles_{current_date_iso_formatted}.xlsx`.

### Server Side

The server-side script offers a REST API using Flask. It accepts a transmitted CSV containing vehicle information, fetches resources from an external API, applies filtering, and returns the result in an appropriate data structure.

#### Steps

1. Authenticate the request towards the [Baubuddy API](https://api.baubuddy.de) using the provided credentials.
2. Accept a transmitted CSV file in a POST call to `/api/upload`.
3. Request resources from `https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active`.
4. Store and merge the API response with the CSV data.
5. Filter out resources that do not have a value set for the `hu` field.
6. For each `labelId` in the vehicle's JSON array `labelIds`, resolve its colorCode using `https://api.baubuddy.de/dev/index.php/v1/labels/{labelId}`.
7. Return the data structure in JSON format.

## Usage

### Client Side

```bash
python try_cli.py -k kurzname info -c 
```

### Run server.py
```
$ python server.py
```

### Open another terminal and run client.py
```
$ python client.py
```
### Dependencies
- Flask
- pandas
- requests
- openpyxl
- flask-cors






















Hello dear python dev!

This repository is supposed to act as a playground for your submission.

Before getting started, please make sure use this repository as a **template** and create your own **public** repository, on which you will commit and push your code regularly. 
Once you are ready, please mail us back the link to your repository. 

Below, you will find the **Task** definition.

Happy Hacking :computer:

# Task

Write two python scripts that have to achieve the common goal to downloads a certain set of resources, merges them with CSV-transmitted resources, and converts them to a formatted excel file.
In particular, the script should:

## Client

Transmits a CSV to a REST-API (s. Server-section below), handles the response and generates an Excel-File taking the input parameters into account.

- Take an input parameter `-k/--keys` that can receive an arbitrary amount of string arguments
- Take an input parameter `-c/--colored` that receives a boolean flag and defaults to `True`

- Transmit CSV containing vehicle information to the POST Call of the server (example data: [vehicles.csv](vehicles.csv))
- Convert the servers response into an excel file that contains all resources and make sure that:
   - Rows are sorted by response field `gruppe`
   - Columns always contain `rnr` field
   - Only keys that match the input arguments are considered as additional columns (i.e. when the script is invoked with `kurzname` and `info`, print two extra columns)
   - If `labelIds` are given and at least one `colorCode` could be resolved, use the first `colorCode` to tint the cell's text (if `labelIds` is given in `-k`)
   - If the `-c` flag is `True`, color each row depending on the following logic:
     - If `hu` is not older than 3 months --> green (`#007500`)
     - If `hu` is not older than 12 months --> orange (`#FFA500`)
     - If `hu` is older than 12 months --> red (`#b30000`)
   - The file should be named `vehicles_{current_date_iso_formatted}.xlsx`

## Server

This script should offer a REST-API, that accepts a CSV, downloads a certain set of resources, merges them with the CSV, applies filtering, and returns them in an appropriate data-structure

- REST-API (e.g. FastAPI, Flask, Django …) offering a POST Call which accepts a transmitted CSV containing vehicle information 
- Upon receiving a valid CSV file, do the following
   - Request the resources located at `https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active`
   - Store both of them (the API Response + request body) in an appropriate data structure and make sure the result is distinct
   - Filter out any resources that do not have a value set for `hu` field
   - For each `labelId` in the vehicle's JSON array `labelIds` resolve its `colorCode` using `https://api.baubuddy.de/dev/index.php/v1/labels/{labelId}`
   - return data-structure in JSON format

### Authorization

It's mandatory for your requests towards the https://api.baubuddy.de to be authorized. You can find the required request below:

This is how it looks in `curl`:

```bash
curl --request POST \
  --url https://api.baubuddy.de/index.php/login \
  --header 'Authorization: Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz' \
  --header 'Content-Type: application/json' \
  --data '{
        "username":"365",
        "password":"1"
}'
```

The response will contain a json object, having the access token in `json["oauth"]["access_token"]`. For all subsequent calls this has to be added to the request headers as `Authorization: Bearer {access_token}`.

A possible implementation in `Python` could be the following. You don't have to copy over this one, feel free to indivualize it or use a different network library.

```python
import requests
url = "https://api.baubuddy.de/index.php/login"
payload = {
    "username": "365",
    "password": "1"
}
headers = {
    "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
    "Content-Type": "application/json"
}
response = requests.request("POST", url, json=payload, headers=headers)
print(response.text)
```
