import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from utils.database import get_db_connection

def get_supplier_features():
    session = get_db_connection()
    
    # Get supplier features from database
    query = """
    SELECT 
        s.supplier_id,
        COUNT(DISTINCT p.product_id) as product_count,
        SUM(od.quantity) as total_sales_quantity,
        AVG(od.unit_price) as avg_sale_price,
        COUNT(DISTINCT o.customer_id) as unique_customers
    FROM suppliers s
    LEFT JOIN products p ON s.supplier_id = p.supplier_id
    LEFT JOIN order_details od ON p.product_id = od.product_id
    LEFT JOIN orders o ON od.order_id = o.order_id
    GROUP BY s.supplier_id
    """
    
    df = pd.read_sql(query, session.get_bind())
    session.close()
    return df

def cluster_suppliers(eps=0.5, min_samples=3):
    # Get supplier features
    df = get_supplier_features()
    
    # Prepare features for clustering
    features = df[['product_count', 'total_sales_quantity', 'avg_sale_price', 'unique_customers']]
    
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
        'product_count': 'mean',
        'total_sales_quantity': 'mean',
        'avg_sale_price': 'mean',
        'unique_customers': 'mean',
        'supplier_id': 'count'
    }).rename(columns={'supplier_id': 'supplier_count'})
    
    return {
        'supplier_clusters': df.to_dict('records'),
        'cluster_analysis': cluster_analysis.to_dict()
    } 