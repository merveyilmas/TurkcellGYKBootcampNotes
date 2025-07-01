import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import tree
import random
import joblib
from fastapi import FastAPI,Request
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI(title="Sales Prediction API")

class Order(BaseModel):
    product_id: int = Field(..., ge=1, le=77, description="Product id değeri 1 ile 77 arasında olmalıdır.")
    unit_price: float
    discount: float
    season: int = Field(..., ge=1, le=4, description="Season değeri 1 ile 4 arasında olmalıdır.")

    
@app.get("/")
def read_root():
    return {"message": "Satış Tahmin API'sine hoş geldiniz."}

@app.post("/predict",tags=["Prediction"])
def predict_approval(order:Order):
    lr_model = joblib.load("LinearReg/sales_prediction_model.pkl")
    input_data = [[order.unit_price, order.discount, order.season, order.product_id]]
    prediction = lr_model.predict(input_data)[0]
    return {
        "prediction" : prediction,
        "details":{
            "product_id":order.product_id,
            "unit_price":order.unit_price,
            "discount":order.discount,
            "season":order.season
        }
    }


# ✅ GLOBAL EXCEPTION HANDLERS

# 1. ValueError handler (örneğin season sınırı dışında)
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"error": "Geçersiz değer", "message": str(exc)}
    )


# 2. ValidationError handler (eksik alan, tip hatası vs.)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "Doğrulama hatası", "details": exc.errors()}
    )


# 3. Genel beklenmeyen tüm hatalar
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Sunucu hatası", "details": str(exc)}
    )