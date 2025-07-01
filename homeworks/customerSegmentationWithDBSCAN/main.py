from fastapi import FastAPI
from problem2.product_clustering import cluster_products
from problem3.supplier_segmentation import cluster_suppliers
from problem4.country_analysis import cluster_countries
from pydantic import BaseModel

app = FastAPI(title="Customer Segmentation API")

class DBSCANParams(BaseModel):
    eps: float = 0.5
    min_samples: int = 5

@app.get("/")
async def root():
    return {"message": "Customer Segmentation API"}

@app.post("/api/v1/product-clusters")
async def get_product_clusters(params: DBSCANParams):
    return cluster_products(eps=params.eps, min_samples=params.min_samples)

@app.post("/api/v1/supplier-clusters")
async def get_supplier_clusters(params: DBSCANParams):
    return cluster_suppliers(eps=params.eps, min_samples=params.min_samples)

@app.post("/api/v1/country-clusters")
async def get_country_clusters(params: DBSCANParams):
    return cluster_countries(eps=params.eps, min_samples=params.min_samples)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 