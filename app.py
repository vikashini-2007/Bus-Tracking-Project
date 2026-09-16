from flask import Flask, render_template, request, redirect, jsonify
import pymysql

app = Flask(__name__)

# ---------------- DATABASE CONNECTION ----------------
def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Vikashini@1989",
        database="bus_tracking"
    )

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template("index.html")

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/login')

    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            return render_template("dashboard.html")
        else:
            return "Invalid Login ❌"

    return render_template("login.html")

# ---------------- ADD ROUTE ----------------
@app.route('/add_route', methods=['GET', 'POST'])
def add_route():
    if request.method == 'POST':
        source = request.form['source']
        destination = request.form['destination']

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO routes(source, destination) VALUES (%s, %s)",
            (source, destination)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return render_template("dashboard.html")

    return render_template("add_route.html")

# ---------------- ADD BUS ----------------
@app.route('/add_bus', methods=['GET', 'POST'])
def add_bus():
    if request.method == 'POST':
        bus_number = request.form['bus_number']
        driver_name = request.form['driver_name']
        route_id = request.form['route_id']

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO buses(bus_number, driver_name, route_id) VALUES (%s, %s, %s)",
            (bus_number, driver_name, route_id)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return render_template("dashboard.html")

    return render_template("add_bus.html")

# ---------------- VIEW BUSES ----------------
@app.route('/buses')
def buses():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT bus_number, driver_name, latitude, longitude
        FROM buses
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("buses.html", buses=data)
@app.route('/edit_bus/<bus_number>', methods=['GET', 'POST'])
def edit_bus(bus_number):

    conn = connect_db()
    cursor = conn.cursor()

    if request.method == 'POST':

        driver_name = request.form['driver_name']
        route_id = request.form['route_id']

        cursor.execute("""
            UPDATE buses
            SET driver_name=%s, route_id=%s
            WHERE bus_number=%s
        """, (driver_name, route_id, bus_number))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect('/buses')

    cursor.execute("""
        SELECT bus_number, driver_name, route_id
        FROM buses
        WHERE bus_number=%s
    """, (bus_number,))

    bus = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("edit_bus.html", bus=bus)
# ---------------- DELETE BUS ----------------
@app.route('/delete_bus/<bus_number>')
def delete_bus(bus_number):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM buses WHERE bus_number=%s",
        (bus_number,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/buses')
# ---------------- MAP PAGE ----------------
@app.route('/map')
def map_view():
    return render_template("map.html")
# ---------------- REST API - GET ALL + POST ----------------

@app.route('/api/buses', methods=['GET', 'POST'])
def api_buses():

    if request.method == 'POST':

        data = request.get_json()

        if not data:
            return jsonify({
                "message": "JSON body is required"
            }), 400

        bus_number = data.get('bus_number')
        driver_name = data.get('driver_name')
        route_id = data.get('route_id')

        if not bus_number or not driver_name or route_id is None:
            return jsonify({
                "message": "bus_number, driver_name and route_id are required"
            }), 400

        conn = connect_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO buses
                (bus_number, driver_name, route_id)
                VALUES (%s, %s, %s)
                """,
                (bus_number, driver_name, route_id)
            )

            conn.commit()

        except pymysql.MySQLError:

            conn.rollback()

            return jsonify({
                "message": "Could not add bus"
            }), 400

        finally:

            cursor.close()
            conn.close()

        return jsonify({
            "message": "Bus added successfully",
            "bus_number": bus_number
        }), 201

    # ---------------- GET ALL BUSES ----------------

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT bus_number, driver_name, latitude, longitude
        FROM buses
        WHERE latitude IS NOT NULL
        AND longitude IS NOT NULL
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    buses_data = []

    for bus in data:

        buses_data.append({
            "bus_number": bus[0],
            "driver_name": bus[1],
            "latitude": float(bus[2]),
            "longitude": float(bus[3])
        })

    return jsonify(buses_data)
# ---------------- GET ONE BUS API ----------------
@app.route('/api/buses/<bus_number>', methods=['GET'])
def get_one_bus(bus_number):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT bus_number, driver_name, route_id, latitude, longitude
        FROM buses
        WHERE bus_number=%s
    """, (bus_number,))

    bus = cursor.fetchone()

    cursor.close()
    conn.close()

    if bus:
        return jsonify({
            "bus_number": bus[0],
            "driver_name": bus[1],
            "route_id": bus[2],
            "latitude": bus[3],
            "longitude": bus[4]
        })

    return jsonify({
        "message": "Bus not found"
    }), 404

# ---------------- UPDATE BUS API ----------------
@app.route('/api/buses/<bus_number>', methods=['PUT'])
def update_bus_api(bus_number):

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "JSON body is required"
        }), 400

    driver_name = data.get('driver_name')
    route_id = data.get('route_id')

    if not driver_name or route_id is None:
        return jsonify({
            "message": "driver_name and route_id are required"
        }), 400

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE buses
        SET driver_name=%s, route_id=%s
        WHERE bus_number=%s
    """, (driver_name, route_id, bus_number))

    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Bus not found"
        }), 404

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Bus updated successfully",
        "bus_number": bus_number
    })
# ---------------- DELETE BUS API ----------------
@app.route('/api/buses/<bus_number>', methods=['DELETE'])
def delete_bus_api(bus_number):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM buses WHERE bus_number=%s",
        (bus_number,)
    )

    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Bus not found"
        }), 404

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Bus deleted successfully",
        "bus_number": bus_number
    })
@app.route('/search_bus', methods=['GET', 'POST'])
def search_bus():

    bus = None

    if request.method == 'POST':

        bus_number = request.form['bus_number']

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT bus_number, driver_name, latitude, longitude
            FROM buses
            WHERE bus_number=%s
            """,
            (bus_number,)
        )

        bus = cursor.fetchone()

        cursor.close()
        conn.close()

    return render_template("search_bus.html", bus=bus)
@app.route('/bus_details', methods=['GET', 'POST'])
def bus_details():

    bus = None

    if request.method == 'POST':

        bus_number = request.form['bus_number']

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                buses.bus_number,
                buses.driver_name,
                routes.source,
                routes.destination,
                buses.latitude,
                buses.longitude
            FROM buses
            JOIN routes
            ON buses.route_id = routes.route_id
            WHERE buses.bus_number = %s
        """, (bus_number,))

        bus = cursor.fetchone()

        cursor.close()
        conn.close()

    return render_template("bus_details.html", bus=bus)
@app.route('/update_location', methods=['GET', 'POST'])
def update_location():

    if request.method == 'POST':

        bus_number = request.form['bus_number']
        latitude = request.form['latitude']
        longitude = request.form['longitude']

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE buses
            SET latitude=%s, longitude=%s
            WHERE bus_number=%s
            """,
            (latitude, longitude, bus_number)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return render_template("update_success.html")

    return render_template("update_location.html")
if __name__ == '__main__':
    app.run(debug=True)