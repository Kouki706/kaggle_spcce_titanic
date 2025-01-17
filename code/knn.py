#k-近傍法（k-nearest neighbor）
#train score = 0.816143
# %%
import pandas as pd
import matplotlib.pyplot as mb
import numpy as np

# %%
train=pd.read_csv('../Data/train.csv')
test=pd.read_csv('../Data/test.csv')
# %%
train.head()
# %%
train.dtypes
# %%
train.isnull().sum()
# %%
test.dtypes
# %%
test.isnull().sum()
# %%
x=train[['Pclass','SibSp','Parch']]
y=train[['Survived']]
# %%
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)
# %%
from sklearn.neighbors import KNeighborsClassifier

knn=KNeighborsClassifier()
knn.fit(x_train, y_train)
# %%
knn.score(x_test, y_test)
# %%
x_for_submit = test[['Pclass', 'SibSp', 'Parch']]
submit = test[['PassengerId']]
submit['Survived']=knn.predict(x_for_submit)

submit
# %%
submit.to_csv('../submission/submit01_knn.csv', index=False)




# %%
#Feature Improvement and Feature Selection
# %%
#Feature addition
# %%
x=train[['Pclass','SibSp','Parch','Sex']]
y=train[['Survived']]
# %%
x=pd.get_dummies(x, dtype=int, columns=['Pclass', 'Sex'])
x
# %%
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)

knn=KNeighborsClassifier()
knn.fit(x_train, y_train)

knn.score(x_test, y_test)
# %%
#Feature addition and removing null
# %%
x=train[['Pclass','SibSp','Parch','Sex','Fare']]
y=train[['Survived']]
# %%
x=pd.get_dummies(x, dtype=int, columns=['Pclass', 'Sex'])
x
# %%
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)

knn=KNeighborsClassifier()
knn.fit(x_train, y_train)

knn.score(x_test, y_test)
# %%
#Standardization
# %%
from sklearn.preprocessing import StandardScaler

scaler=StandardScaler()
scaler.fit(x_train)

x_train_scaled=scaler.transform(x_train)
x_test_scaled=scaler.transform(x_test)

knn=KNeighborsClassifier()
knn.fit(x_train_scaled, y_train)

knn.score(x_test_scaled, y_test)
# %%
x_for_submit = test[['Pclass', 'SibSp', 'Parch', 'Sex', 'Fare']]
submit = test[['PassengerId']]

x_for_submit=pd.get_dummies(x_for_submit, columns=['Pclass', 'Sex'])

x_for_submit['Fare']=x_for_submit['Fare'].fillna(x_for_submit['Fare'].mean())

#scaler.fitはtrainに対してfitさせたものをtestに使うのがポイント
#ただし、今回の場合はtestにfitさせたものでpredictしたほうがスコアは良かった
scaler=StandardScaler()
scaler.fit(x_train)

x_for_submit_scaled=scaler.transform(x_for_submit)

submit['Survived']=knn.predict(x_for_submit_scaled)
submit
# %%
submit.to_csv('../submission/submit02_knn.csv', index=False)
# %%
