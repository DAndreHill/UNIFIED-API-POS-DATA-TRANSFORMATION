
# ingestion.py

import requests
import xml.etree.ElementTree as ET

from config import ITEMS_URL, ORDERS_SOAP_URL


SOAP_XML_PAYLOAD = """<soapenv:Envelope
xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
xmlns:ser="http://localhost:5000/service">
    <soapenv:Header/>
    <soapenv:Body>
        <ser:list_orders/>
    </soapenv:Body>
</soapenv:Envelope>"""


def fetch_items():
    """Retrieve items using REST/JSON."""
    print(f"Fetching items from {ITEMS_URL}...")

    response = requests.get(ITEMS_URL, timeout=10)
    response.raise_for_status()

    return response.json()


def fetch_orders_soap():
    """Retrieve orders using SOAP/XML."""
    print(f"Fetching orders from {ORDERS_SOAP_URL}...")

    response = requests.post(
        ORDERS_SOAP_URL,
        headers={"Content-Type": "text/xml"},
        data=SOAP_XML_PAYLOAD.encode("utf-8"),
        timeout=10
    )

    response.raise_for_status()

    root = ET.fromstring(response.content)

    def local_name(element):
        return element.tag.split("}")[-1]

    orders = []

    for order_elem in root.iter():
        if local_name(order_elem) != "OrderSchema":
            continue

        def get_text(tag):
            for child in order_elem:
                if local_name(child) == tag:
                    return child.text.strip() if child.text else None
            return None

        order = {
            "id": get_text("id"),
            "sku_id": get_text("sku_id"),
            "sku_name": get_text("sku_name"),
            "quantity": get_text("quantity"),
            "unit_price": get_text("unit_price"),
            "total_price": get_text("total_price"),
            "currency": get_text("currency"),
            "status": get_text("status"),
            "transaction_date": get_text("transaction_date")
        }

        orders.append(order)

    return orders
