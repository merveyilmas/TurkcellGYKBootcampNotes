import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix, ConfusionMatrixDisplay, classification_report
from sklearn import tree
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(42)
def generateData(m=2000):
    data=[]
    for _ in range(2000):
        age = np.random.randint(18,65)
        income = round(np.random.randint(3000,30000),2)
        debt = np.random.randint(0, 50000)
        credit_score = np.random.randint(0,1000)
        employment_years = np.random.randint(0,40)
        approved = 1 if (income > 8000 and credit_score > 600 and debt < 20000 and employment_years > 2 and age < 55) else 0
        data.append([age, income, debt, credit_score, employment_years, approved])
    return pd.DataFrame(data, columns=['age', 'income', 'debt', 'credit_score', 'employment_years','approved'])

df1 = generateData()
 

X = df1[['age', 'income', 'debt', 'credit_score', 'employment_years']]
y = df1['approved']

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=50 ,random_state=42)
model.fit(X_train, y_train)

y_prediction = model.predict(X_test)

#Modelin başarı değerlendirmesi
print(f'Accuracy f1: {f1_score(y_test, y_prediction)}')
accuracy = accuracy_score(y_test, y_prediction)
print(f"Accuracy: {accuracy:.2f}")

#Ilk karar ağacı görselleştirmesi
plt.figure(figsize=(20, 10))
tree.plot_tree(model.estimators_[0], 
               feature_names=['age', 'income', 'debt', 'credit_score', 'employment_years'],
               class_names=['Rejected', 'Approved'],
               filled=True,
               rounded=True)
plt.title("Random Forest - 1. Karar Ağacı")
plt.show()

#Kredi Onay Dağılımı
plt.figure(figsize=(6,4))
sns.countplot(data=df1, x='approved')
plt.title("Kredi Onay Dağılımı")
plt.xticks([0,1], ['Reddedildi', 'Onaylandı'])
plt.show()

#Confusion matrix görselleştirmesi
cm = confusion_matrix(y_test, y_prediction)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Reddedildi', 'Onaylandı'])

plt.figure(figsize=(6,6))
disp.plot(cmap=plt.cm.Blues, values_format='d')
plt.title("Karışıklık Matrisi")
plt.grid(False)
plt.show()

#Classification report
report = classification_report(y_test, y_prediction, target_names=['Reddedildi', 'Onaylandı'])
print("Sınıflandırma Raporu")
print(report)

#Tahmin sonuçlarının görsel karşılaştırması
comparison_df = pd.DataFrame({
    'Gerçek': y_test,
    'Tahmin': y_prediction
})

real_counts = comparison_df['Gerçek'].value_counts().sort_index()
pred_counts = comparison_df['Tahmin'].value_counts().sort_index()

labels = ['Reddedildi', 'Onaylandı']

x = np.arange(len(labels))
width = 0.35

plt.figure(figsize=(8,6))
plt.bar(x - width/2, real_counts, width, label='Gerçek')
plt.bar(x + width/2, pred_counts, width, label='Tahmin')

plt.xticks(x, labels)
plt.ylabel("Sayı")
plt.title("Gerçek ve Tahmin Edilen Sınıfların Dağılımı")
plt.legend()
plt.grid(axis='y')
plt.show()