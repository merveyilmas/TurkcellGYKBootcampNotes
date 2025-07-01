from sqlalchemy import create_engine,text

class Database:
    
    def __init__(self):
        self.engine = create_engine("postgresql://postgres:12345@localhost/GYK1Northwind")
        # burayı kendi bilgilerinize göre düzenlemeniz gerekir. postgres:şifre@localhost...

    def get_customers(self):
        with self.engine.connect() as conn:
            query = text("SELECT * FROM customers")
            result = conn.execute(query)
            return result.fetchall()
        
    def get_orders(self):
        with self.engine.connect() as conn:
            query = text("SELECT * FROM orders")
            result = conn.execute(query)
            return result.fetchall()
        
    def get_products(self):
        with self.engine.connect() as conn:
            query = text("SELECT * FROM products")
            result = conn.execute(query)
            return result.fetchall()
        
        
    def get_categories(self):
         with self.engine.connect() as conn:
             query = text("SELECT * FROM categories")
             result = conn.execute(query)
             return result.fetchall()
     

    def get_order_details(self):
        with self.engine.connect() as conn:
            query = text("SELECT * FROM order_details")
            result = conn.execute(query)
            return result.fetchall()
        
    def get_orders_with_details(self):
        with self.engine.connect() as conn:
            query = text("""SELECT o.order_id,p.product_id,od.unit_price,od.quantity,od.discount,cs.customer_id,o.order_date,c.category_id,cs.city,cs.region,cs.country
                            FROM order_details AS od 
                            JOIN orders AS o on o.order_id = od.order_id
                            JOIN products AS p on p.product_id = od.product_id
                            JOIN categories AS c on p.category_id = c.category_id
                            JOIN customers as cs on cs.customer_id = o.customer_id
                    """)
            result = conn.execute(query)
            return result.fetchall()
    
    def get_company(self):
        with self.engine.connect() as conn:
            query = text("""
                        SELECT 
                            o.order_id, 
                            o.employee_id, 
                            c.country AS customer_country,
                            o.order_date, 
                            od.quantity, 
                            s.company_name AS shipper
                        FROM orders o
                        JOIN order_details od ON o.order_id = od.order_id
                        JOIN customers c ON o.customer_id = c.customer_id
                        JOIN shippers s ON o.ship_via = s.shipper_id;
                """)
            result = conn.execute(query)
            return result.fetchall()
        
    

    def close(self):
        self.engine.dispose()

