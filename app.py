from flask import Flask, jsonify
from datetime import datetime, timedelta
from models import db, Company, Warehouse, Product, Inventory, Supplier, ProductSupplier, Sales

app = Flask(__name__)

# Database configuration (SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ---------------- HOME ROUTE ---------------- #

@app.route('/')
def home():
    return "Bynry Backend Case Study Running "


# ---------------- LOW STOCK ALERT API ---------------- #

@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def low_stock_alerts(company_id):
    try:
        alerts = []
        recent_date = datetime.utcnow() - timedelta(days=30)

        # Get all inventories for company warehouses
        inventories = db.session.query(Inventory)\
            .join(Warehouse)\
            .filter(Warehouse.company_id == company_id)\
            .all()

        for inv in inventories:
            product = Product.query.get(inv.product_id)

            # Skip if product not found
            if not product:
                continue

            # Check recent sales
            recent_sales = Sales.query.filter(
                Sales.product_id == product.id,
                Sales.created_at >= recent_date
            ).count()

            if recent_sales == 0:
                continue

            threshold = product.low_stock_threshold

            # Check low stock condition
            if inv.quantity < threshold:

                # Get supplier (first match)
                supplier = db.session.query(Supplier)\
                    .join(ProductSupplier, Supplier.id == ProductSupplier.supplier_id)\
                    .filter(ProductSupplier.product_id == product.id)\
                    .first()

                alerts.append({
                    "product_id": product.id,
                    "product_name": product.name,
                    "sku": product.sku,
                    "warehouse_id": inv.warehouse_id,
                    "warehouse_name": inv.warehouse.name if inv.warehouse else None,
                    "current_stock": inv.quantity,
                    "threshold": threshold,
                    "days_until_stockout": 10,  # simplified assumption
                    "supplier": {
                        "id": supplier.id if supplier else None,
                        "name": supplier.name if supplier else None,
                        "contact_email": supplier.contact_email if supplier else None
                    }
                })

        return jsonify({
            "alerts": alerts,
            "total_alerts": len(alerts)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- RUN SERVER ---------------- #

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables automatically

    app.run(debug=True)

with app.app_context():
    db.create_all()

    # Add sample data ONLY if empty
    if not Company.query.first():
        company = Company(name="Demo Company")
        db.session.add(company)
        db.session.commit()

        warehouse = Warehouse(name="Main Warehouse", company_id=company.id)
        db.session.add(warehouse)
        db.session.commit()

        product = Product(name="Widget A", sku="WID-001", price=100, low_stock_threshold=20)
        db.session.add(product)
        db.session.commit()

        inventory = Inventory(product_id=product.id, warehouse_id=warehouse.id, quantity=5)
        db.session.add(inventory)

        supplier = Supplier(name="Supplier Corp", contact_email="orders@supplier.com")
        db.session.add(supplier)
        db.session.commit()

        ps = ProductSupplier(product_id=product.id, supplier_id=supplier.id)
        db.session.add(ps)

        sale = Sales(product_id=product.id, warehouse_id=warehouse.id, quantity=2)
        db.session.add(sale)

        db.session.commit()