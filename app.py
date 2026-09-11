import pymysql
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

app.secret_key = "simple-secret-key"


PER_PAGE = 5


def get_connection():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="rootroot",   
        database="contact_app",
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


@app.route("/")
def index():
    search = request.args.get("search", "")

    page_text = request.args.get("page", "1")
    try:
        page = int(page_text)
    except ValueError:
        page = 1

    if page < 1:
        page = 1

    
    offset = (page - 1) * PER_PAGE

    connection = get_connection()
    cursor = connection.cursor()

   
    search_pattern = "%" + search + "%"

    
    cursor.execute(
        "SELECT COUNT(*) AS total FROM contacts WHERE name LIKE %s",
        (search_pattern,)
    )
    total_contacts = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT * FROM contacts WHERE name LIKE %s ORDER BY id LIMIT %s OFFSET %s",
        (search_pattern, PER_PAGE, offset)
    )
    contacts = cursor.fetchall()

    cursor.close()
    connection.close()

    total_pages = (total_contacts + PER_PAGE - 1) // PER_PAGE
    if total_pages < 1:
        total_pages = 1

    return render_template(
        "index.html",
        contacts=contacts,
        search=search,
        page=page,
        total_pages=total_pages
    )


@app.route("/add", methods=["GET", "POST"])
def add_contact():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        phone = request.form["phone"].strip()

        # Basic validation
        if name == "":
            flash("Name cannot be empty.")
            return redirect(url_for("add_contact"))

        if email == "":
            flash("Email cannot be empty.")
            return redirect(url_for("add_contact"))

        if phone == "":
            flash("Phone cannot be empty.")
            return redirect(url_for("add_contact"))

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO contacts (name, email, phone) VALUES (%s, %s, %s)",
            (name, email, phone)
        )
        connection.commit()
        cursor.close()
        connection.close()

        flash("Contact added successfully!")
        return redirect(url_for("index"))

    return render_template("add_contact.html")


@app.route("/edit/<int:contact_id>", methods=["GET", "POST"])
def edit_contact(contact_id):
    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        phone = request.form["phone"].strip()

        if name == "" or email == "" or phone == "":
            flash("Name, email, and phone cannot be empty.")
            cursor.close()
            connection.close()
            return redirect(url_for("edit_contact", contact_id=contact_id))

        cursor.execute(
            "UPDATE contacts SET name = %s, email = %s, phone = %s WHERE id = %s",
            (name, email, phone, contact_id)
        )
        connection.commit()
        cursor.close()
        connection.close()

        flash("Contact updated successfully!")
        return redirect(url_for("index"))

    cursor.execute("SELECT * FROM contacts WHERE id = %s", (contact_id,))
    contact = cursor.fetchone()
    cursor.close()
    connection.close()

    if contact is None:
        flash("Contact not found.")
        return redirect(url_for("index"))

    return render_template("edit_contact.html", contact=contact)


@app.route("/delete/<int:contact_id>")
def delete_contact(contact_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
    connection.commit()
    cursor.close()
    connection.close()

    flash("Contact deleted successfully!")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
