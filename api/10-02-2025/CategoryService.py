import requests

baseUrl = "http://localhost:3000/categories"

def createCategory(product):
    response = requests.post(baseUrl, json=product)
    return response.json()

categoryToCreate = {"id": 1, "name": "Yazılım", "description": "Yazılım ile ilgili kurslar"}
createCategory(categoryToCreate)