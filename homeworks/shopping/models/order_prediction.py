import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.preprocessing import StandardScaler
import numpy as np
from database import get_db
import pandas as pd
from datetime import datetime, timedelta

class OrderPredictionModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.load_data()
        self.train_model()

    def load_data(self):
        db = next(get_db())
        # Query to get customer order history
        query = """
        SELECT 
            c.CustomerID,
            COUNT(o.OrderID) as order_count,
            SUM(od.Quantity * od.UnitPrice) as total_spent,
            AVG(od.Quantity * od.UnitPrice) as avg_order_size,
            MAX(o.OrderDate) as last_order_date
        FROM Customers c
        LEFT JOIN Orders o ON c.CustomerID = o.CustomerID
        LEFT JOIN [Order Details] od ON o.OrderID = od.OrderID
        GROUP BY c.CustomerID
        """
        
        df = pd.read_sql(query, db.connection())
        
        # Create target variable: 1 if customer ordered in last 6 months, 0 otherwise
        six_months_ago = datetime.now() - timedelta(days=180)
        df['target'] = (pd.to_datetime(df['last_order_date']) > six_months_ago).astype(int)
        
        # Prepare features
        self.X = df[['total_spent', 'order_count', 'avg_order_size']].fillna(0)
        self.y = df['target']
        
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

        # Handle class imbalance
        class_weights = {0: 1, 1: len(self.y[self.y == 0]) / len(self.y[self.y == 1])}
        
        self.model.fit(
            self.X, self.y,
            epochs=50,
            batch_size=32,
            validation_split=0.2,
            class_weight=class_weights
        )

    def predict(self, customer_id: str, total_spent: float, order_count: int, avg_order_size: float):
        # Prepare input data
        input_data = np.array([[total_spent, order_count, avg_order_size]])
        input_data = self.scaler.transform(input_data)
        
        # Make prediction
        prediction = self.model.predict(input_data)[0][0]
        
        return {
            "will_order": bool(prediction > 0.5),
            "probability": float(prediction)
        } 