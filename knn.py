# -*- coding: utf-8 -*-
"""KNN.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Wpdjbji49URUGOSfOk5emp-9KBjWohOy
"""

# We assume that similar thing exist in close or near to each other
# Example: Girls hostel and Biys Hostel
# girls are similar to girls so all girls are in girls hostel and vise versa
# items that are closer to each other----similar to each other
# K is the number of neighbours we are going to consider
# To avoid conflict K must be odd number

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("/content/wisc_bc_data.csv")
df.head()

"""### Benign and Malignent
Benign are the cells that are cancerous and Malignent are cells that are't cancerous
"""

df.dtypes

df['diagnosis'] = df['diagnosis'].astype('category')

df.dtypes

df['diagnosis'].value_counts()

df = df.drop(labels='id', axis=1)
df

X = df.drop(labels='diagnosis', axis=1)
Y=df['diagnosis']

"""## Standerize the Data"""

from scipy.stats import zscore
xScale = X.apply(zscore)
xScale.describe()     # std dev  of all is 1

xScaled_df = pd.DataFrame(xScale)
xScaled_df

"""# Building Knn Model"""

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(xScaled_df, Y, test_size=0.3, random_state=1)

from sklearn.neighbors import KNeighborsClassifier
KNN = KNeighborsClassifier(n_neighbors=5, weights='distance')

KNN.fit(x_train, y_train)

KNN_Predict = KNN.predict(x_test)
KNN_Predict

KNN.score(x_test, y_test)

from sklearn import metrics

print("Confusion Matrics: ")

cm = metrics.confusion_matrix(y_test, KNN_Predict, labels=['M', 'B'])
df_cm = pd.DataFrame(cm, index=[i for i in ['M', 'B']], columns=[i for i in ['Predicted M', 'Predicted B']])
sns.heatmap(df_cm, annot=True)
plt.show

"""# Choosing K"""

from sklearn.model_selection import cross_val_score

score_1 = []

for i in range(1,50):
  KNN_2=KNeighborsClassifier(n_neighbors=i)
  score_2 = cross_val_score(KNN_2, xScaled_df, Y, cv=10)    # cv=10 means 10 iterations and then take mean of it
  score_1.append(score_2.mean())

score_1

plt.figure(figsize=(20,10))

plt.plot(range(1,50), score_1, color='blue', linestyle='dashed', marker='o', markerfacecolor='red', markersize=10)

plt.title("Accuracy Rate VS K-Vlaues")
plt.xlabel('K')
plt.ylabel('Accuracy')