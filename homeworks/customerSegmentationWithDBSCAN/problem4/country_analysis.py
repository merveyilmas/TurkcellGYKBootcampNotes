import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from utils.database import get_db_connection

def get_country_features():
    session = get_db_connection()
    
    # Get country features from database
    query = """
    WITH order_product_counts AS (
        SELECT 
            o.order_id,
            COUNT(*) as products_in_order
        FROM orders o
        JOIN order_details od ON o.order_id = od.order_id
        GROUP BY o.order_id
    )
    SELECT 
        c.country,
        COUNT(DISTINCT o.order_id) as total_orders,
        AVG(od.unit_price * od.quantity) as avg_order_amount,
        AVG(opc.products_in_order) as avg_products_per_order
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN order_details od ON o.order_id = od.order_id
    LEFT JOIN order_product_counts opc ON o.order_id = opc.order_id
    GROUP BY c.country
    """
    
    df = pd.read_sql(query, session.get_bind())
    session.close()
    return df

def cluster_countries(eps=0.5, min_samples=3):
    # Get country features
    df = get_country_features()
    
    # Prepare features for clustering
    features = df[['total_orders', 'avg_order_amount', 'avg_products_per_order']]
    
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
        'total_orders': 'mean',
        'avg_order_amount': 'mean',
        'avg_products_per_order': 'mean',
        'country': 'count'
    }).rename(columns={'country': 'country_count'})
    
    return {
        'country_clusters': df.to_dict('records'),
        'cluster_analysis': cluster_analysis.to_dict()
    } 