from flask import Flask, request

import mysql.connector

app = Flask(__name__)


def connect_db():
    return mysql.connector.connect(
        host="mysql-service",
        user="root",
        password="root",
        database="studentdb"
    )


@app.route("/")
def home():
    return """
    <h1>Student Registration</h1>

    <form action="/register" method="POST">

        <label>Name:</label>
        <input type="text" name="name" required>
        <br><br>

        <label>Course:</label>
        <input type="text" name="course" required>
        <br><br>

        <label>Email:</label>
        <input type="email" name="email" required>
        <br><br>

        <button type="submit">Register</button>

    </form>

    <br>

    <a href="/students">View Registered Students</a>
    """


@app.route("/register", methods=["POST"])
def register():

    name = request.form["name"]
    course = request.form["course"]
    email = request.form["email"]

    db = connect_db()
    cursor = db.cursor()

    query = """
        INSERT INTO students (name, course, email)
        VALUES (%s, %s, %s)
    """

    cursor.execute(query, (name, course, email))

    db.commit()

    cursor.close()
    db.close()

    return """
    <h2>Registration Successful! ✅</h2>
    <a href="/">Register Another Student</a>
    <br><br>
    <a href="/students">View Students</a>
    """


@app.route("/students")
def students():

    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT id, name, course, email FROM students")

    rows = cursor.fetchall()

    cursor.close()
    db.close()

    result = "<h1>Registered Students</h1>"

    for row in rows:
        result += f"""
        <p>
        {row[0]} - {row[1]} - {row[2]} - {row[3]}
        </p>
        """

    result += '<br><a href="/">Back to Registration</a>'

    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)