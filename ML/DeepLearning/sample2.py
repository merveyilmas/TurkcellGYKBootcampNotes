import numpy as np
import tensorflow as tf
import matplotlib as plt
from sklearn.preprocessing import StandardScaler

# ages 
X = np.array([5,6,7,8,9,10], dtype=float).reshape(-1, 1)

# heigths
Y = np.array([110,116,123,130,136,142], dtype=float).reshape(-1, 1)

# verilerimizi bilgisayarın anlamdırabilmesi için ölçeklendiriyoruz
x_scaler = StandardScaler()
y_scaler = StandardScaler()

X_scaled = x_scaler.fit_transform(X)
Y_scaled = y_scaler.fit_transform(Y)

# katman sayısını deneme yanılma yöntemi ile buluruz
model = tf.keras.Sequential([
    tf.keras.layers.Dense(units=10, activation="relu",input_shape=[1]), # 1. katman
    tf.keras.layers.Dense(units=1), # 2. katman

])

model.compile(optimizer="adam",loss="mean_squared_error")

# modeli eğitiyoruz
# epochs; verinin üzerinden 50 kere geç ki iyice öğren 
model.fit(X_scaled, Y_scaled, epochs=500, verbose=0)

test_age = np.array([[7.5]])
test_age_scaled = x_scaler.transform(test_age)

prediction_height_scaled = model.predict(np.array([test_age_scaled]))

prediction_height = y_scaler.inverse_transform(prediction_height_scaled)
print(f"{test_age} için boy tahmini = {prediction_height}")