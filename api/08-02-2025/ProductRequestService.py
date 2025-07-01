import requests

baseUrl = "http://localhost:3000/products" 

def getProducta():
    response = requests.get(baseUrl)
    return response.json()

#for product in getProducta():
#    print(product.get("name"), "/", product.get("unitPrice"))

def getProductsByCategory(categoryId):
    response = requests.get(baseUrl + "/?categoryId=" + str(categoryId))
    return response

#for product in getProductsByCategory(6):
#    print(product.get("name"), "/", product.get("unitPrice"))

def createProduct(product):
    response = requests.post(baseUrl, json=product)
    return response.json()

#productToCreate = {"supliedId": 2, "categoryId": 6, "unitPrice": 969, "name": "Kalem"}
#createProduct(productToCreate)

def updateProduct(id, product):
    response = requests.put(baseUrl + "/" + str(id), json=product)
    return response.json()

# put ile update yaptığımızda mevcut datalar kayıp olur, yerini sadece bizim parametreler alır

#productToUpdate = {"supplierId": 2, "categoryId": 6, "unitPrice": 567, "name": "Kalem"}
#updateProduct("5", productToUpdate)

def updateProductByPatch(id, product):
    response = requests.patch(baseUrl + "/" + str(id), json=product)
    return response.json()

# patch ile update yaptığımızda mevcut datalar kayıp olmaz, ilgili alanlar güncellenir sadece

#productToUpdate = {"supplierId": 2, "categoryId": 6, "unitPrice": 567, "name": "Kalem 100"}
#updateProduct("6", productToUpdate)