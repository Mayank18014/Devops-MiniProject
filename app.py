'''from flask import Flask, render_template, request, jsonify, session, redirect
import pymysql

app = Flask(__name__)

# 🔐 SECRET KEY (SESSION KE LIYE)
app.secret_key = "my_super_secret_key_123"

# ---------------- DATABASE CONNECTION ----------------
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="product_scanner",
        cursorclass=pymysql.cursors.Cursor
    )

# ---------------- HOME PAGE ----------------
@app.route('/')
def index():
    return render_template('index.html')

# ---------------- SCAN PRODUCT ----------------
@app.route('/scan', methods=['POST'])
def scan_product():
    data = request.get_json()
    barcode = data.get('barcode')

    conn = get_db_connection()
    cur = conn.cursor()

    # save scan history
    cur.execute("INSERT INTO scan_history (barcode) VALUES (%s)", (barcode,))
    conn.commit()

    # check product
    cur.execute("SELECT * FROM products WHERE barcode = %s", (barcode,))
    product = cur.fetchone()

    cur.close()
    conn.close()

    if product:
        return jsonify({
            "status": "success",
            "product": {
                "barcode": product[1],
                "name": product[2],
                "brand": product[3],
                "mfg": str(product[4]),
                "exp": str(product[5]),
                "price": float(product[6]),
                "description": product[7]
            }
        })
    else:
        return jsonify({
            "status": "fake",
            "message": "Product not registered / unverified"
        })

# ---------------- ADMIN LOGIN ----------------
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # demo credentials
        if username == "admin" and password == "admin123":
            session['admin'] = True
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": "Invalid credentials"})

    return render_template('admin_login.html')

# ---------------- ADMIN PAGE (ADD PRODUCT) ----------------
@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect('/admin-login')
    return render_template('admin.html')

# ---------------- ADD PRODUCT ----------------
@app.route('/add-product', methods=['POST'])
def add_product():
    if not session.get('admin'):
        return jsonify({"status": "error", "message": "Unauthorized"})

    data = request.get_json()

    barcode = data.get('barcode')
    name = data.get('product_name')
    brand = data.get('brand')
    mfg = data.get('manufacturing_date')
    exp = data.get('expiry_date')
    price = data.get('price')
    desc = data.get('description')

    if not barcode or not name:
        return jsonify({
            "status": "error",
            "message": "Barcode and product name required"
        })

    conn = get_db_connection()
    cur = conn.cursor()

    # check duplicate barcode
    cur.execute("SELECT id FROM products WHERE barcode = %s", (barcode,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({
            "status": "error",
            "message": "Barcode already exists"
        })

    cur.execute("""
        INSERT INTO products
        (barcode, product_name, brand, manufacturing_date, expiry_date, price, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (barcode, name, brand, mfg, exp, price, desc))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "Product added successfully"
    })

# ---------------- PRODUCT LIST ----------------
@app.route('/products')
def products():
    if not session.get('admin'):
        return redirect('/admin-login')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, barcode, product_name, brand, price FROM products")
    data = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('products.html', products=data)

# ---------------- DELETE PRODUCT ----------------
@app.route('/delete-product/<int:pid>', methods=['POST'])
def delete_product(pid):
    if not session.get('admin'):
        return jsonify({"status": "error"})

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM products WHERE id = %s", (pid,))
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"status": "success"})

# ---------------- SCAN HISTORY ----------------
@app.route('/scan-history')
def scan_history():
    if not session.get('admin'):
        return redirect('/admin-login')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT barcode, scan_time FROM scan_history ORDER BY scan_time DESC")
    data = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("scan_history.html", history=data)

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/admin-login')

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)'''

from flask import Flask, render_template, request, jsonify, Response
from flask_mysqldb import MySQL
from datetime import datetime
import time

# ---------------- PROMETHEUS IMPORTS ----------------
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# ---------------- DATABASE CONFIG ----------------
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "product_scanner"
}

# ---------------- PROMETHEUS METRICS ----------------
REQUEST_COUNT = Counter(
    "product_scanner_requests_total",
    "Total number of HTTP requests"
)

REQUEST_LATENCY = Histogram(
    "product_scanner_request_latency_seconds",
    "Request latency in seconds"
)

# ---------------- DATABASE CONNECTION ----------------
def get_db_connection():
    return mysql.connector.connect(**db_config)

# ---------------- PROMETHEUS METRICS ENDPOINT ----------------
@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# ---------------- HOME PAGE ----------------
@app.route("/")
def index():
    REQUEST_COUNT.inc()
    start_time = time.time()

    response = render_template("index.html")

    REQUEST_LATENCY.observe(time.time() - start_time)
    return response

# ---------------- ADMIN LOGIN ----------------
@app.route("/admin")
def admin():
    REQUEST_COUNT.inc()
    start_time = time.time()

    response = render_template("admin_login.html")

    REQUEST_LATENCY.observe(time.time() - start_time)
    return response

# ---------------- SCAN PRODUCT ----------------
@app.route("/scan", methods=["POST"])
def scan_product():
    REQUEST_COUNT.inc()
    start_time = time.time()

    data = request.get_json()
    barcode = data.get("barcode")

    conn = get_db_connection()
    cur = conn.cursor()

    # Store scan history
    cur.execute(
        "INSERT INTO scan_history (barcode, scanned_at) VALUES (%s, %s)",
        (barcode, datetime.now())
    )
    conn.commit()

    # Fetch product
    cur.execute("SELECT * FROM products WHERE barcode = %s", (barcode,))
    product = cur.fetchone()

    cur.close()
    conn.close()

    REQUEST_LATENCY.observe(time.time() - start_time)

    if product:
        return jsonify({
            "status": "success",
            "product": {
                "barcode": product[1],
                "name": product[2],
                "brand": product[3],
                "mfg": str(product[4]),
                "exp": str(product[5]),
                "price": float(product[6]),
                "description": product[7]
            }
        })
    else:
        return jsonify({
            "status": "fake",
            "message": "Product not registered / unverified"
        })

# ---------------- VIEW SCAN HISTORY ----------------
@app.route("/history")
def scan_history():
    REQUEST_COUNT.inc()
    start_time = time.time()

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM scan_history ORDER BY scanned_at DESC")
    history = cur.fetchall()

    cur.close()
    conn.close()

    response = render_template("scan_history.html", history=history)

    REQUEST_LATENCY.observe(time.time() - start_time)
    return response

# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

