from sklearn import linear_model, datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression, Lasso, Ridge
import matplotlib.pyplot as plt
import random
import matplotlib
import numpy as np
import copy

#获得data和label
def load_data():
    data = []
    deas = []
    data1 = []
    with open('processed.cleveland.data','r') as f:
        m = f.readlines()
        st = ''
        for i in range(len(m)-3):
            arr = m[i].split(',')
            #data1.append(1.0)
            for n in range(len(arr)-2):
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
test_data = copy.deepcopy(m)
test_label = copy.deepcopy(n)
#print('lenm',len(test_data))
for i in range(100):
    rand = random.randint(0,299)
    #print(rand)
    train_data.append(m[rand])
    label_data.append(n[rand])
    #test_data.remove(m[rand])
    #test_label.remove(n[rand])

#print(len(train_data))
#print(label_data)


#测试精度
def accurancy(m,n,linreg):
    wei = linreg.coef_
    result = linreg.intercept_
    tr = 0
    fa = 0
    for j in range(len(m)):
        for i in range(len(m[0])):
            result += wei[i] * m[j][i]
            #print(result)

        if result >= 0.5and int(n[j]) == 1:
            tr += 1
        elif result < 0.5 and int(n[j]) == 0:
            tr += 1
        else:
            fa += 1
        result = linreg.intercept_
    #print(fa+tr)
    #print(tr / (tr + fa))
    return tr/(tr+fa)

#画图
def mat(x_axis, y_axis):
    #print(x_axis)
    #print(y_axis)
    #x = np.linspace(0, 1, 20)
    for i in range(len(x_axis)-1):
        plt.plot(x_axis, y_axis, color='r')
    plt.show()
    return 0
#进行训练lasso
'''
def skl(X,Y):
    alpha = 0.001
    lasso = Lasso(max_iter=10000, alpha=alpha)
    linreg = lasso.fit(X, Y)
    return linreg
'''
#进行训练linear
def lassoRegession(x, y, test, lab):
    data = []
    label = []
    x_axis = []
    y_axis = []
    linreg = LinearRegression()
    linreg.fit(x, y)
    #return linreg
    for i in range(0,len(x),5):
        for j in x[i:i+5]:
            data.append(j)
        for t in y[i:i+5]:
            label.append(t)
        linreg.fit(data, label)
        x_axis.append(i + 5)#,accurancy(test, lab, linreg)])
        y_axis.append(accurancy(test, lab, linreg))
    #print('x_axis',x_axis)
    #print('y_axis',y_axis)
    w = mat(x_axis, y_axis)
    return linreg
linreg = lassoRegession(train_data,label_data,m,n)
print(linreg)
acc = accurancy(m,n,linreg)
print(acc)
'''
def predict(age, sex, chest, rest, serum, sugar, electro, heart_rate, angina, oldpeak, slope, vessels, weights, inter):
    result = age*weights[0] + sex * weights[1] + chest * weights[2] + \
             rest * weights[3] + serum * weights[4] + sugar * weights[5] + \
             electro * weights[6] + heart_rate * weights[7] +  angina * weights[8] + \
             oldpeak * weights[9] +  slope * weights[10] +  vessels * weights[11] + inter
    if result >= 0.5:
        return 1
    else:
        return 0
'''
