
# etl_core.py

import hashlib
import json
import datetime

from ingestion import fetch_items, fetch_orders_soap
from models import Session, UnifiedRecord


def transform_sku_id(sku_id):
    """Convert a source SKU ID into the unified string format."""
    return f"SPTBG-{int(sku_id)}"


def normalize_item(item):
    return {
        "source_type": "items",
        "sku_id": transform_sku_id(item["id"]),
        "sku_name": item.get("name"),
        "quantity": int(item.get("quantity_on_hand", 0)),
        "unit_price": float(item.get("price", 0)),
        "total_price": float(item.get("price", 0)),
        "currency": item.get("currency", "USD"),
        "status": "available",
        "transaction_date": datetime.datetime.fromisoformat(
            item["created"]
        ),
        "raw_payload_hash": hashlib.md5(
            json.dumps(item, sort_keys=True).encode()
        ).hexdigest()
    }


def normalize_order(order):
    try:
        txn_date = (
            datetime.datetime.fromisoformat(order["transaction_date"])
            if order.get("transaction_date")
            else None
        )
    except ValueError:
        txn_date = None

    return {
        "source_type": "orders",
        "sku_id": transform_sku_id(order["sku_id"]),
        "sku_name": order.get("sku_name", ""),
        "quantity": int(order.get("quantity", 0)),
        "unit_price": float(order.get("unit_price", 0)),
        "total_price": float(order.get("total_price", 0)),
        "currency": order.get("currency", "USD"),
        "status": order.get("status", "unknown"),
        "transaction_date": txn_date,
        "raw_payload_hash": hashlib.md5(
            json.dumps(order, sort_keys=True).encode()
        ).hexdigest()
    }


def load_to_db(records):
    session = Session()

    try:
        for payload in records:
            record = UnifiedRecord(**payload)
            session.add(record)

        session.commit()
        print(f"Successfully loaded {len(records)} records.")

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def run_etl():
    print("--- Starting ETL Pipeline ---")

    items = fetch_items()
    item_records = [normalize_item(item) for item in items]

    orders = fetch_orders_soap()
    order_records = [normalize_order(order) for order in orders]

    if not items or not orders:
        raise ValueError("Source API returned no items or orders.")

    print("Loading transformed records...")
    load_to_db(item_records + order_records)

    print("--- ETL Pipeline Complete ---")
