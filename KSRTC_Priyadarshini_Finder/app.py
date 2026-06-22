from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    stops = [
        "Palakkad", "Olavakkode", "Kanjikode", "Walayar",
        "Mundur", "Kongad", "Kalladikode", "Karimba",
        "Mannarkkad", "Kumaramputhur", "Perinthalmanna",
        "Ottapalam", "Shoranur", "Cherpulassery", "Pattambi",
        "Vaniamkulam", "Parli", "Pathiripala", "Mankara",
        "Koduvayur", "Alathur", "Vadakkencherry","Vandithavalam", "Kuzhalmannam",
        "Nemmara", "Kollengode", "Chittur", "Tattamangalam",
        "Meenakshipuram", "Pollachi", "Kozhikode", "Thrissur",
        "Agali", "Attappadi", "Alanallur", "Govindapuram","Nelliyampathy",
        "Pothundi Dam","Velanthavalam","Kozhinjampara","Kallepulli"
         
    ]

    stops = sorted(list(set(stops)))
    return render_template("index.html", stops=stops)


@app.route('/search', methods=['POST'])
def search():
    stop = request.form["stop"]

    conn = sqlite3.connect("buses.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM buses
        WHERE stops LIKE ?
           OR end_point LIKE ?
           OR route_name LIKE ?
           OR start_point LIKE ?
    """, (f"%{stop}%", f"%{stop}%", f"%{stop}%", f"%{stop}%"))

    buses = cursor.fetchall()
    conn.close()

    eligible_types = [
        "shuttle",
        "city ordinary",
        "priyadarshini",
        "ordinary",
        "regular fast",
        "limited stop ordinary",
        "town-to-town",
        "fair stage ordinary",
        "point to point ordinary",
        "gramavandi"
    ]

    processed_buses = []

    for bus in buses:
        bus_type = str(bus[5]).lower().strip()
        eligible = any(t in bus_type for t in eligible_types)

        processed_buses.append({
            "bus_no": bus[0],
            "route_name": bus[1],
            "start_point": bus[2],
            "end_point": bus[3],
            "timing": bus[4],
            "bus_type": bus[5],
            "stops": bus[6],
            "eligible": eligible
        })

    return render_template(
        "results.html",
        buses=processed_buses,
        stop=stop
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)