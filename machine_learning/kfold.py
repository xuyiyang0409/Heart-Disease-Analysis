from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression, Lasso
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import accuracy_score

import sys
sys.path.append('../')
from backend.db_handler import DBHandler


# obtain data and label
def load_data():
    data = []
    deas = []
    data1 = []
    with open('../data/processed.cleveland.data','r') as f:
        m = f.readlines()
        for i in range(len(m)-3):
            arr = m[i].split(',')
            for n in range(len(arr)-2):
                if n == 2 or n == 7 or n == 8 or n == 9 or n == 11:
                    if arr[n] == '?':
                        data1.append(0.0)
                    else:
                        data1.append(float(arr[n]))
            data.append(data1)
            data1 = []
            if int(arr[-1][0]) == 0:
                deas.append(float(arr[-1][0]))
            else:
                deas.append(1.0)
    return data, deas


m,n = load_data()

train_data = []
label_data = []
test_data = m[299:]
test_label = n[299:]
for i in range(299):
    train_data.append(m[i])
    label_data.append(n[i])


# test accuracy
def accurancy(m,n,linreg):
    wei = linreg.coef_
    result = linreg.intercept_
    tr = 0
    fa = 0
    for j in range(len(m)):
        for i in range(len(m[0])):
            result += wei[i] * m[j][i]
        if result >= 0.5 and int(n[j]) == 1:
            tr += 1
        elif result < 0.5 and int(n[j]) == 0:
            tr += 1
        else:
            fa += 1
        result = linreg.intercept_
    return tr/(tr+fa)

# plot
def mat(x_axis, y_axis):
    plt.title("Linear Regression")
    plt.plot(x_axis, y_axis, linewidth=3, color='r', marker='o', markersize=10)
    plt.xlabel('Number of training data')
    plt.ylabel('Accuracy')
    plt.text(x_axis[-1], y_axis[-1], y_axis[-1], ha='right', va='bottom', fontsize=12)
    plt.savefig('../data/LR.png')
    plt.show()
    return 0


def ridgeRegession(x, y, m, n):
    # L2 linear regression, add sum of square loss based on linear model
    model = svm.SVC()
    alpha = {'kernel':('linear','rbf'),'C':[0.01,0.02,0.03,0.035, 0.04],'gamma' : [0.000001,0.0002,0.03,0.04,0.05]}
    # 5-fold cross validation
    ridge_model = GridSearchCV(model, alpha, cv = 10)
    ridge_model = ridge_model.fit(x, y)
    print('best_params:%s' % ridge_model.best_params_)
    best_model = ridge_model.best_estimator_
    y_pred = best_model.predict(m)
    print('accuracy', accuracy_score(n, y_pred))
    return ridge_model


def acc(lab, be):
    tr = 0
    fa = 0
    for i in range(len(be)):
        if be[i] >= 0.5 and lab[i] == 1:
            tr+= 1
        elif be[i] < 0.5 and lab[i] == 0:
            tr+= 1
        else:
            fa+= 1
    acc = tr/(tr+fa)
    return acc


# training linear
def lassoRegession(x, y, test, lab):
    # L1 linear regression, add abs loss based on linear model
    model = Lasso()
    alpha = np.logspace(-3, 2, 10)
    # 5-fold cross validation
    lasso_model = GridSearchCV(model, param_grid={'alpha': alpha}, cv=5)
    lasso_model.fit(x, y)
    best = lasso_model.best_estimator_
    be = best.predict(test)
    acc(lab,be)
    return lasso_model


lassoRegession(train_data,label_data,test_data,test_label)


def acc2(test,label, coe, inter):
    tr = 0
    fa = 0
    result = inter
    for j in range(len(test)):
        for i in range(len(m[0])):
            result += coe[i] * test[j][i]
        if result >= 0.5 and int(label[j]) == 1:
            tr += 1
        elif result < 0.5 and int(label[j]) == 0:
            tr += 1
        else:
            fa += 1
        result = inter
    return tr / (tr + fa)


def jiaocha(x,y,test,lab):
    final_coe = []
    final_int = []
    x_axis = []
    y_axis = []
    for o in range(25,len(x),25):
        accur = []
        coe = []
        inter = []
        w = x[0:o]
        q = y[0:o]
        t = len(w) / 5
        t = int(t)
        for i in range(0, len(w), t):

            test_data = w[i:i + t]
            test_la = q[i:i+t]
            train = w[0:i]
            train_la = q[0:i]
            for j in w[i + t:]:
                train.append(j)
            for n in q[i+t:]:
                train_la.append(n)
            model = LinearRegression()
            model.fit(train,train_la)
            coe.append(model.coef_)
            inter.append(model.intercept_)
            re = model.predict(test_data)
            a = acc(test_la,re)
            print('Coefficient: ',model.coef_)
            print('Accuracy: ',accur)
            accur.append(a)
        for p in range(len(accur)):
            if max(accur) == accur[p]:
                final_coe.append(coe[p])
                final_int.append(inter[p])
                break
        x_axis.append(o)
        y_axis.append(max(accur))
        result = acc2(test, lab, final_coe[-1], final_int[-1])
        print('Accc',result)
    mat(x_axis,y_axis)
    print(final_coe[-1])
    print(final_int[-1])
    return final_coe[-1],final_int[-1]


coe,inter = jiaocha(train_data,label_data,test_data,test_label)
fin_coe = [coe[-1],coe[-2],coe[1],coe[0],coe[2]]

print('[K-ford] Final coefficients')
print(fin_coe)


db_handler = DBHandler()
db_handler.database_controller(f'DELETE FROM Predict;')
db_handler.database_controller(f'INSERT INTO Predict VALUES'
                               f'({fin_coe[0]}, {fin_coe[1]}, {fin_coe[2]}, {fin_coe[3]}, {fin_coe[4]}, {inter});')


