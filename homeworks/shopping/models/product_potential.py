import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Embedding, Flatten
from sklearn.preprocessing import LabelEncoder, StandardScaler
import numpy as np
from database import get_db
import pandas as pd

class ProductPotentialModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.category_encoder = LabelEncoder()
        self.load_data()
        self.train_model()

    def load_data(self):
        db = next(get_db())
        # Query to get customer category spending
        query = """
        SELECT 
            o.CustomerID,
            c.CategoryName,
            SUM(od.Quantity * od.UnitPrice) as category_spending
        FROM Orders o
        JOIN [Order Details] od ON o.OrderID = od.OrderID
        JOIN Products p ON od.ProductID = p.ProductID
        JOIN Categories c ON p.CategoryID = c.CategoryID
        GROUP BY o.CustomerID, c.CategoryName
        """
        
        df = pd.read_sql(query, db.connection())
        
        # Pivot the data to get category spending as features
        df_pivot = df.pivot(index='CustomerID', columns='CategoryName', values='category_spending').fillna(0)
        
        # Get all unique categories
        self.categories = df_pivot.columns.tolist()
        
        # Prepare features
        self.X = df_pivot.values
        self.y = self.category_encoder.fit_transform(df_pivot.index)
        
        # Scale features
        self.X = self.scaler.fit_transform(self.X)

    def train_model(self):
        self.model = Sequential([
            Dense(128, activation='relu', input_shape=(len(self.categories),)),
            Dropout(0.3),
            Dense(64, activation='relu'),
            Dropout(0.2),
            Dense(32, activation='relu'),
            Dense(len(self.categories), activation='softmax')
        ])

        self.model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )

        self.model.fit(
            self.X, self.y,
            epochs=50,
            batch_size=32,
            validation_split=0.2
        )

    def predict(self, customer_id: str, category_spending: dict, new_product_category: str):
        # Prepare input data
        input_data = np.zeros(len(self.categories))
        for category, spending in category_spending.items():
            if category in self.categories:
                idx = self.categories.index(category)
                input_data[idx] = spending
        
        # Scale the input
        input_data = self.scaler.transform([input_data])
        
        # Make prediction
        predictions = self.model.predict(input_data)[0]
        
        # Get top 3 recommended categories
        top_categories = []
        for idx, prob in enumerate(predictions):
            top_categories.append({
                "category": self.categories[idx],
                "probability": float(prob)
            })
        
        # Sort by probability
        top_categories.sort(key=lambda x: x["probability"], reverse=True)
        
        return {
            "new_product_potential": float(predictions[self.categories.index(new_product_category)]),
            "top_recommendations": top_categories[:3]
        } 