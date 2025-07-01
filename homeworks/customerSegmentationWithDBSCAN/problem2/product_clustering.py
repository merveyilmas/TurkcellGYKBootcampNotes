#“Benzer sipariş geçmişine sahip ürünleri DBSCAN ile gruplandırın. Az satılan ya da alışılmadık kombinasyonlarda geçen ürünleri belirleyin.”

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from utils.database import get_db_connection

def get_product_features():
    session = get_db_connection()
    
    # Get product features from database
    query = """
    SELECT 
        p.product_id,
        AVG(od.unit_price) as avg_price,
        COUNT(od.order_id) as order_frequency,
        AVG(od.quantity) as avg_quantity_per_order,
        COUNT(DISTINCT o.customer_id) as unique_customers
    FROM products p
    LEFT JOIN order_details od ON p.product_id = od.product_id
    LEFT JOIN orders o ON od.order_id = o.order_id
    GROUP BY p.product_id
    """
    
    df = pd.read_sql(query, session.get_bind())
    session.close()
    return df

def cluster_products(eps=0.5, min_samples=5):
    # Get product features
    df = get_product_features()
    
    # Prepare features for clustering
    features = df[['avg_price', 'order_frequency', 'avg_quantity_per_order', 'unique_customers']]
    
    # Scale features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    
    # Perform DBSCAN clustering
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    clusters = dbscan.fit_predict(scaled_features)
    
    # Add cluster labels to dataframe
    df['cluster'] = clusters
    
    # Analyze clusters
    cluster_analysis = df.groupby('cluster').agg({
        'avg_price': 'mean',
        'order_frequency': 'mean',
        'avg_quantity_per_order': 'mean',
        'unique_customers': 'mean',
        'product_id': 'count'
    }).rename(columns={'product_id': 'product_count'})
    
    return {
        'product_clusters': df.to_dict('records'),
        'cluster_analysis': cluster_analysis.to_dict()
    } 