from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from models.order_prediction import OrderPredictionModel
from models.return_risk import ReturnRiskModel
from models.product_potential import ProductPotentialModel

app = FastAPI(title="Shopping Prediction API",
             description="API for predicting customer behavior in shopping",
             version="1.0.0")

# Initialize models
order_model = OrderPredictionModel()
return_risk_model = ReturnRiskModel()
product_potential_model = ProductPotentialModel()

class OrderPredictionRequest(BaseModel):
    customer_id: str
    total_spent: float
    order_count: int
    avg_order_size: float

class ReturnRiskRequest(BaseModel):
    customer_id: str
    discount_rate: float
    product_quantity: int
    total_amount: float

class ProductPotentialRequest(BaseModel):
    customer_id: str
    category_spending: dict
    new_product_category: str

@app.post("/predict/order")
async def predict_order(request: OrderPredictionRequest):
    try:
        prediction = order_model.predict(
            customer_id=request.customer_id,
            total_spent=request.total_spent,
            order_count=request.order_count,
            avg_order_size=request.avg_order_size
        )
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/return-risk")
async def predict_return_risk(request: ReturnRiskRequest):
    try:
        prediction = return_risk_model.predict(
            customer_id=request.customer_id,
            discount_rate=request.discount_rate,
            product_quantity=request.product_quantity,
            total_amount=request.total_amount
        )
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/product-potential")
async def predict_product_potential(request: ProductPotentialRequest):
    try:
        prediction = product_potential_model.predict(
            customer_id=request.customer_id,
            category_spending=request.category_spending,
            new_product_category=request.new_product_category
        )
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 