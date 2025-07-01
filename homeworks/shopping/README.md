# Shopping Prediction API

This API provides three machine learning models for predicting customer behavior in shopping:

1. Order Prediction: Predicts if a customer will place an order in the next 6 months
2. Return Risk: Predicts the risk of a product being returned
3. Product Potential: Predicts the potential of a customer buying a new product category

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your database connection in a `.env` file:
```
DATABASE_URL=your_database_connection_string
```

3. Run the API:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Order Prediction
**Endpoint:** `/predict/order`
**Method:** POST
**Request Body:**
```json
{
    "customer_id": "string",
    "total_spent": 1000.0,
    "order_count": 5,
    "avg_order_size": 200.0
}
```

### 2. Return Risk
**Endpoint:** `/predict/return-risk`
**Method:** POST
**Request Body:**
```json
{
    "customer_id": "string",
    "discount_rate": 0.1,
    "product_quantity": 2,
    "total_amount": 50.0
}
```

### 3. Product Potential
**Endpoint:** `/predict/product-potential`
**Method:** POST
**Request Body:**
```json
{
    "customer_id": "string",
    "category_spending": {
        "Beverages": 100.0,
        "Confections": 50.0
    },
    "new_product_category": "Dairy Products"
}
```

## Model Details

### Order Prediction Model
- Uses customer's total spending, order count, and average order size
- Predicts probability of ordering in next 6 months
- Handles class imbalance with weighted loss

### Return Risk Model
- Uses discount rate, product quantity, and total amount
- Provides SHAP explanations for predictions
- Cost-sensitive learning with higher weights for returns

### Product Potential Model
- Uses customer's spending history across categories
- Provides top 3 recommended categories
- Multi-label prediction with softmax output

## Example Usage

```python
import requests

# Order Prediction
response = requests.post("http://localhost:8000/predict/order", json={
    "customer_id": "ALFKI",
    "total_spent": 1000.0,
    "order_count": 5,
    "avg_order_size": 200.0
})
print(response.json())

# Return Risk
response = requests.post("http://localhost:8000/predict/return-risk", json={
    "customer_id": "ALFKI",
    "discount_rate": 0.1,
    "product_quantity": 2,
    "total_amount": 50.0
})
print(response.json())

# Product Potential
response = requests.post("http://localhost:8000/predict/product-potential", json={
    "customer_id": "ALFKI",
    "category_spending": {
        "Beverages": 100.0,
        "Confections": 50.0
    },
    "new_product_category": "Dairy Products"
})
print(response.json())
``` 