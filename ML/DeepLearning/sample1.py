import numpy as np

# nem oranına göre dışarı çıkmalı mıyım, çıkmamalı mıyım?

# inputs
temprature = 20
humidity = 60

X = np.array([temprature,humidity])

# noron weigths, sıcaklık - nem
weigths = np.array([0.4,0.6])

# eşik değer, bias - önyargılar, tensorflow bias ı otomatik hesaplıyor bizim ayarlamamıma gerek yok
bias = -20

# noron çıktısı(output)
# dot iki vektörün iç çarpımını toplar verir; - 20 ile 0.4 ü çarpıp, 60 ile de 0.6 yı çarpıp toplayıp + bias
output = np.dot(X,weigths) + bias

print("Nöronun ham çıktısı", output)

def sigmoid(x):
    return 1/(1+np.exp(-x))

activated_output = sigmoid(output)

print("Nöronun aktivasyon sonrası çıktısı", activated_output)
