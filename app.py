from flask import Flask, render_template, request, redirect
import os
import pymysql
import boto3
import uuid
from dotenv import load_dotenv

load_dotenv()
s3 = boto3.client("s3", region_name="ap-south-1")
S3_BUCKET = "student-management-images-2026-hr"

app = Flask(__name__)


def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )


@app.route("/")
def home():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.close()
    connection.close()

    for student in students:
        if student["image_url"]:
            student["image_url"] = s3.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": S3_BUCKET,
                    "Key": student["image_url"]
                },
                ExpiresIn=3600
            )

    return render_template("index.html", students=students)


@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"]
    email = request.form["email"]
    course = request.form["course"]
    age = request.form["age"]

    image = request.files.get("image")
    image_url = None

    if image and image.filename:
        filename = f"{uuid.uuid4()}_{image.filename}"

        s3.upload_fileobj(
            image,
            S3_BUCKET,
            filename,
            ExtraArgs={"ContentType": image.content_type}
        )

        image_url = filename

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO students (name, email, course, age, image_url)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (name, email, course, age, image_url)
    )

    connection.commit()
    cursor.close()
    connection.close()

    return redirect("/")
@app.route("/edit/<int:student_id>")
def edit_student(student_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE student_id = %s",
        (student_id,)
    )

    student = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template("edit.html", student=student)


@app.route("/update/<int:student_id>", methods=["POST"])
def update_student(student_id):
    name = request.form["name"]
    email = request.form["email"]
    course = request.form["course"]
    age = request.form["age"]

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE students
        SET name = %s, email = %s, course = %s, age = %s
        WHERE student_id = %s
        """,
        (name, email, course, age, student_id)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/")


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE student_id = %s",
        (student_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/")


@app.route("/upload-photo/<int:student_id>", methods=["POST"])
def upload_photo(student_id):
    image = request.files.get("image")

    if not image or not image.filename:
        return redirect("/")

    filename = f"{uuid.uuid4()}_{image.filename}"

    s3.upload_fileobj(
        image,
        S3_BUCKET,
        filename,
        ExtraArgs={"ContentType": image.content_type or "application/octet-stream"}
    )

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE students SET image_url = %s WHERE student_id = %s",
        (filename, student_id)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return redirect("/")


@app.route("/students")
def students():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return str(students)

@app.route("/remove-photo/<int:student_id>", methods=["POST"])
def remove_photo(student_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT image_url FROM students WHERE student_id = %s",
        (student_id,)
    )
    student = cursor.fetchone()

    if student and student["image_url"]:
        s3.delete_object(
            Bucket=S3_BUCKET,
            Key=student["image_url"]
        )

        cursor.execute(
            "UPDATE students SET image_url = NULL WHERE student_id = %s",
            (student_id,)
        )
        connection.commit()

    cursor.close()
    connection.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
