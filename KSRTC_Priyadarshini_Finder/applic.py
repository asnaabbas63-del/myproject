from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    stops = [
        "Olavakkode",
        "Mundur",
        "Kongad",
        "Kalladikode",
        "Thachampara",
        "Mannarkkad",
        "Ottapalam",
        "Shornur",
        "Chittur",
        "Kanjikode"
    ]
    return render_template("index.html", stops=stops)

@app.route('/search', methods=['POST'])
def search():
    stop = request.form['stop']

    conn = sqlite3.connect("buses.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM buses
        WHERE stops LIKE ? OR end_point LIKE ?
    """, (f"%{stop}%", f"%{stop}%"))

    buses = cursor.fetchall()
    conn.close()

    return render_template("results.html", buses=buses,stop=stop)

if __name__ == "__main__":
    app.run(debug=True)