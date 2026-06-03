from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# --- DATABASE ---
def get_db():
    conn = pymysql.connect(
        host="localhost",
        user="zaid",
        password="ZexO@1234",
        database="imwiki",
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn


def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artikler (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tittel VARCHAR(255) NOT NULL,
            innhold TEXT NOT NULL
        )
    """)
    db.commit()
    db.close()

# --- SIDER ---

# Forside: viser alle artikler
@app.route("/")
def forside():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM artikler ORDER BY tittel")
    artikler = cursor.fetchall()
    db.close()
    return render_template("forside.html", artikler=artikler)

# Vis én artikkel
@app.route("/artikkel/<int:id>")
def vis_artikkel(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM artikler WHERE id = %s", (id,))
    artikkel = cursor.fetchone()
    db.close()
    if artikkel is None:
        return "Artikkel ikke funnet", 404
    return render_template("artikkel.html", artikkel=artikkel)

# Ny artikkel
@app.route("/ny", methods=["GET", "POST"])
def ny_artikkel():
    if request.method == "POST":
        tittel = request.form["tittel"]
        innhold = request.form["innhold"]
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO artikler (tittel, innhold) VALUES (%s, %s)", (tittel, innhold))
        db.commit()
        db.close()
        return redirect(url_for("forside"))
    return render_template("ny.html")

# Rediger artikkel
@app.route("/rediger/<int:id>", methods=["GET", "POST"])
def rediger(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM artikler WHERE id = %s", (id,))
    artikkel = cursor.fetchone()
    if request.method == "POST":
        tittel = request.form["tittel"]
        innhold = request.form["innhold"]
        cursor.execute("UPDATE artikler SET tittel = %s, innhold = %s WHERE id = %s", (tittel, innhold, id))
        db.commit()
        db.close()
        return redirect(url_for("vis_artikkel", id=id))
    db.close()
    return render_template("rediger.html", artikkel=artikkel)

# Slett artikkel
@app.route("/slett/<int:id>")
def slett(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM artikler WHERE id = %s", (id,))
    db.commit()
    db.close()
    return redirect(url_for("forside"))

# Start appen
if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0")