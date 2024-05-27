from flask import Flask, render_template, request, url_for, flash, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "crudPY"

mysql = MySQL(app)

@app.route("/")
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', students=data)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        mysql.connection.commit()
        cur.close()
        flash("Data Inserted Successfully")
        return redirect(url_for('index'))

@app.route("/delete/<int:id_data>", methods=['GET'])
def delete(id_data):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
        mysql.connection.commit()
        cur.close()
        flash("Record has been deleted successfully")
    except Exception as e:
        flash(str(e))
    return redirect(url_for("index"))

@app.route("/update", methods=['POST'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                        UPDATE students SET name=%s, email=%s, phone=%s
                        WHERE id=%s
                        """, (name, email, phone, id_data))
            mysql.connection.commit()
            cur.close()
            flash("Data updated successfully")
        except Exception as e:
            flash(str(e))
        return redirect(url_for("index"))
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)