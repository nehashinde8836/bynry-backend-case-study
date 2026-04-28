# Bynry Backend Case Study - Inventory Management System

## Overview
This project implements a simplified backend system for a B2B inventory platform ("StockFlow"). It focuses on low-stock alert generation across multiple warehouses while ensuring clean architecture and scalability.

This project demonstrates backend API design, database modeling, and real-world problem solving for inventory systems.

---

## Case Study Document
Detailed explanation of all parts (Code Review, Database Design, API Implementation):

🔗 https://docs.google.com/document/d/14W19i3oM8S53VSmO322R_wtfYoM1l0AukOQ0HRnVVgs/edit?usp=sharing

---

## Features
- Multi-warehouse inventory tracking
- Low-stock alert API
- Supplier mapping for reordering
- Handles recent sales filtering

---

## Tech Stack
- Python
- Flask
- SQLite
- SQLAlchemy

---

## Setup Instructions

1. Clone the repository:
git clone https://github.com/nehashinde8836/bynry-backend-case-study.git

2. Navigate to project:
cd bynry-backend-case-study

3. Install dependencies:
pip install -r requirements.txt

4. Run the application:
python app.py

---

## API Endpoint

GET /api/companies/{company_id}/alerts/low-stock

Example:
http://127.0.0.1:5000/api/companies/1/alerts/low-stock

---

## Sample Response

{
  "alerts": [
    {
      "product_id": 1,
      "product_name": "Widget A",
      "sku": "WID-001",
      "warehouse_id": 1,
      "warehouse_name": "Main Warehouse",
      "current_stock": 5,
      "threshold": 20,
      "days_until_stockout": 10,
      "supplier": {
        "id": 1,
        "name": "Supplier Corp",
        "contact_email": "orders@supplier.com"
      }
    }
  ],
  "total_alerts": 1
}

---

## Assumptions
- Recent sales defined as last 30 days
- Default low stock threshold = 10
- Each product has at least one supplier
- Single primary supplier considered

---

## Edge Cases Handled
- No recent sales → product ignored
- Missing supplier → handled safely
- Empty inventory → returns empty response
- Invalid company → returns empty alerts

---

## Design Considerations
- Supports multi-warehouse inventory
- Uses relational schema with constraints
- Avoids duplicate inventory entries
- Scalable for large datasets (can add pagination & caching)
- Added indexing considerations on frequently queried fields such as sku, product_id, and warehouse_id to improve performance

---

## Future Improvements
- Add authentication & authorization
- Add pagination for large datasets
- Integrate caching (Redis)
- Predict stockout using analytics/ML

---

## Author
Neha Shinde

---

## Note
This implementation focuses on simplicity, clean backend design, and production-ready practices while making reasonable assumptions due to incomplete requirements.

---

## 📸 Output Screenshots

### API Response
![API Response](Output/api_response.png)

### Server Running
![Server Running](Output/server_running.png)
