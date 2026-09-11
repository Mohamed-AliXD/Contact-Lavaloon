# Contact Management App

A simple Flask + MySQL app for managing contacts, with search and pagination.

## Setup

1. Run `database_setup.sql` in MySQL to create the database and table.
2. Open `app.py` and replace `YOUR_MYSQL_PASSWORD` with your MySQL password.
3. Install dependencies:

```bash
pip install flask pymysql
```

## Run

```bash
python app.py
```

Open `http://127.0.0.1:5000/` in your browser.

## Routes

- `/` — view all contacts (supports `?search=` and `?page=`)
- `/add` — add a new contact
- `/edit/<id>` — edit a contact
- `/delete/<id>` — delete a contact
