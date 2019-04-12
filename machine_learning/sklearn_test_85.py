from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
def load_data():
    data = []
    deas = []
    data1 = []
    with open('processed.cleveland.data','r') as f:
        m = f.readlines()
        st = ''
        for i in m:
            arr = i.split(',')
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
    #print(data)
    #for i in data:
        #print(i)
    #print('deas',deas)
    return data, deas
m,n = load_data()
print(np.shape(m))
print(np.shape(n))

def skl(X,Y):
    linreg = LinearRegression()
    linreg.fit(X, Y)
    return linreg
linreg = skl(m,n)
#print(linreg.intercept_)
#print(linreg.coef_)
wei = linreg.coef_
result = linreg.intercept_



#测试精度
def accurancy(m,n,linreg):
    wei = linreg.coef_
    result = linreg.intercept_
    tr = 0
    fa = 0
    #print(wei)
    #print(len(m))
    for j in range(len(m)):
        for i in range(len(m[0])):
            result += wei[i] * m[j][i]
            #print(result)

        if result >= 0.5 and int(n[j]) == 1:
            tr += 1
        elif result < 0.5 and int(n[j]) == 0:
            tr += 1
        else:
            fa += 1
        result = linreg.intercept_
    #print(fa+tr)
    #print(tr / (tr + fa))
    return tr/(tr+fa)

def predict(age, sex, chest, rest, serum, sugar, electro, heart_rate, angina, oldpeak, slope, vessels, weights, inter):
    result = age*weights[0] + sex * weights[1] + chest * weights[2] + \
             rest * weights[3] + serum * weights[4] + sugar * weights[5] + \
             electro * weights[6] + heart_rate * weights[7] +  angina * weights[8] + \
             oldpeak * weights[9] +  slope * weights[10] +  vessels * weights[11] + inter
    if result >= 0.5:
        return 1
    else:
        return 0
