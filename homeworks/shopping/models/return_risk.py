import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.preprocessing import StandardScaler
import numpy as np
from database import get_db
import pandas as pd
import shap

class ReturnRiskModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.explainer = None
        self.load_data()
        self.train_model()

    def load_data(self):
        db = next(get_db())
        # Query to get order details with discount information
        query = """
        SELECT 
            o.CustomerID,
            od.Discount,
            od.Quantity,
            (od.Quantity * od.UnitPrice * (1 - od.Discount)) as total_amount
        FROM [Order Details] od
        JOIN Orders o ON od.OrderID = o.OrderID
        """
        
        df = pd.read_sql(query, db.connection())
        
        # Create synthetic return labels based on high discount and low amount
        df['is_return'] = ((df['Discount'] > 0.2) & (df['total_amount'] < 100)).astype(int)
        
        # Prepare features
        self.X = df[['Discount', 'Quantity', 'total_amount']]
        self.y = df['is_return']
        
        # Scale features
        self.X = self.scaler.fit_transform(self.X)

    def train_model(self):
        self.model = Sequential([
            Dense(64, activation='relu', input_shape=(3,)),
            Dropout(0.2),
            Dense(32, activation='relu'),
            Dropout(0.2),
            Dense(1, activation='sigmoid')
        ])

        self.model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )

        # Handle class imbalance with higher weight for returns
        class_weights = {0: 1, 1: 5}
        
        self.model.fit(
            self.X, self.y,
            epochs=50,
            batch_size=32,
            validation_split=0.2,
            class_weight=class_weights
        )
        
        # Initialize SHAP explainer
        self.explainer = shap.KernelExplainer(self.model.predict, self.X[:100])

    def predict(self, customer_id: str, discount_rate: float, product_quantity: int, total_amount: float):
        # Prepare input data
        input_data = np.array([[discount_rate, product_quantity, total_amount]])
        input_data = self.scaler.transform(input_data)
        
        # Make prediction
        prediction = self.model.predict(input_data)[0][0]
        
        # Get SHAP values for explanation
        shap_values = self.explainer.shap_values(input_data)
        
        return {
            "return_risk": float(prediction),
            "risk_level": "High" if prediction > 0.7 else "Medium" if prediction > 0.3 else "Low",
            "explanation": {
                "discount_impact": float(shap_values[0][0][0]),
                "quantity_impact": float(shap_values[0][0][1]),
                "amount_impact": float(shap_values[0][0][2])
            }
        } 