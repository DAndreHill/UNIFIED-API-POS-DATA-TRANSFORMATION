
# app.py

from flask import Flask, jsonify, request
from models import Session, UnifiedRecord
from etl_core import run_etl

app = Flask(__name__)


@app.route("/api/unified/records", methods=["GET"])
def get_records():
    session = Session()

    try:
        source = request.args.get("source_type")
        query = session.query(UnifiedRecord)

        if source:
            query = query.filter_by(source_type=source)

        records = [
            {
                "id": r.id,
                "source_type": r.source_type,
                "sku_id": r.sku_id,
                "sku_name": r.sku_name,
                "quantity": r.quantity,
                "unit_price": r.unit_price,
                "total_price": r.total_price,
                "currency": r.currency,
                "status": r.status,
                "transaction_date": (
                    r.transaction_date.isoformat()
                    if r.transaction_date else None
                ),
                "created_at": (
                    r.created_at.isoformat()
                    if r.created_at else None
                )
            }
            for r in query.all()
        ]

        return jsonify(records)

    finally:
        session.close()


@app.route("/api/unified/trigger-etl", methods=["POST"])
def trigger_etl():
    try:
        run_etl()
        return jsonify({
            "message": "ETL pipeline executed successfully."
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
