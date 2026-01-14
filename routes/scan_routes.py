from flask import Blueprint, request, jsonify
from models.product_model import get_product_by_barcode

scan_bp = Blueprint('scan', __name__)

@scan_bp.route('/scan', methods=['POST'])
def scan_product():
    barcode = request.json.get('barcode')

    if not barcode:
        return jsonify({"status": "error", "message": "Barcode missing"})

    from app import mysql
    product = get_product_by_barcode(mysql, barcode)

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
                "desc": product[7]
            }
        })
    else:
        return jsonify({
            "status": "fake",
            "message": "Product not registered. Possible fake!"
        })
