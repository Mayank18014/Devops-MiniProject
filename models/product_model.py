def get_product_by_barcode(mysql, barcode):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE barcode = %s", (barcode,))
    data = cur.fetchone()
    cur.close()
    return data
