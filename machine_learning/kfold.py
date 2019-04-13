from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn import svm, datasets
from sklearn.model_selection import cross_val_score, cross_val_predict
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
import random
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression, Lasso, Ridge
import numpy as np
import copy
from db_handler import DBHandler
import sqlite3
from sklearn.metrics import accuracy_score
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



#测试精度
def accurancy(m,n,linreg):
    wei = linreg.coef_
    result = linreg.intercept_
    tr = 0
    fa = 0
    for j in range(len(m)):
        for i in range(len(m[0])):
            result += wei[i] * m[j][i]
        if result >= 0.5and int(n[j]) == 1:
            tr += 1
        elif result < 0.5 and int(n[j]) == 0:
            tr += 1
        else:
            fa += 1
        result = linreg.intercept_
    return tr/(tr+fa)

#画图
def mat(x_axis, y_axis):
    plt.figure(figsize=(16, 8))
    plt.title("linear accurancy")
    plt.plot(x_axis, y_axis, label='accurancy changes', linewidth=3, color='r', marker='o',
             markerfacecolor='blue', markersize=20)
    plt.xlabel('training number')
    plt.ylabel('accurancy')
    plt.text(x_axis[-1], y_axis[-1], y_axis[-1], ha='right', va='bottom', fontsize=15)
    plt.show()
    return 0





def ridgeRegession(x, y, m, n):
    # L2回归模型，即在线性模型的基础之增加平方和损失
    model = svm.SVC()
    alpha = {'kernel':('linear','rbf'),'C':[0.01,0.02,0.03,0.035, 0.04],'gamma' : [0.000001,0.0002,0.03,0.04,0.05]}
    # 采用5折交叉验证
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
#进行训练linear
def lassoRegession(x, y, test, lab):
    # L1回归模型，即在线性模型的基础之增加绝对值和损失
    model = Lasso()
    alpha = np.logspace(-3, 2, 10)
    # 采用5折交叉验证
    lasso_model = GridSearchCV(model, param_grid={'alpha': alpha}, cv=5)
    lasso_model.fit(x, y)
    #print('best_params:%s' % lasso_model.best_params_)
    best = lasso_model.best_estimator_
    #print(best)
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
        #print(result)
        result = inter
    return tr / (tr + fa)



def jiaocha(x,y,test,lab):
    final_coe = []
    final_int = []
    accur = []
    coe = []
    inter = []
    train = []
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
            #print('test',test_data)
            #print('train',train)
            model = LinearRegression()
            model.fit(train,train_la)
            coe.append(model.coef_)
            inter.append(model.intercept_)
            re = model.predict(test_data)
            #print('re',re)
            a = acc(test_la,re)
            print('coe',model.coef_)
            print('a',accur)
            accur.append(a)
            test_la = []
            test_data = []
            train = []
            train_la = []
        for p in range(len(accur)):
            if max(accur) == accur[p]:
                final_coe.append(coe[p])
                final_int.append(inter[p])
                break
        print(final_int)
        print(final_coe)
        x_axis.append(o)
        y_axis.append(max(accur))
        result = acc2(test, lab, final_coe[-1], final_int[-1])
        print('accc',result)
    mat(x_axis,y_axis)
    print(final_coe[-1])
    print(final_int[-1])
    return final_coe[-1],final_int[-1]



coe,inter = jiaocha(train_data,label_data,test_data,test_label)
fin_coe = [coe[-1],coe[-2],coe[1],coe[0],coe[2]]




connection = sqlite3.connect('a3.db')
cursor = connection.cursor()
cursor.execute('DROP TABLE IF EXISTS Predict;')

cursor.execute('CREATE TABLE IF NOT EXISTS Predict(ca float, oldpeak float, thal float, cp float, exang float, inter float);')
db_handler = DBHandler()
db_handler.database_controller(f'INSERT INTO Predict(ca,oldpeak,thal,cp,exang,inter) VALUES({fin_coe[0]}, {fin_coe[1]}, {fin_coe[2]}, {fin_coe[3]}, {fin_coe[4]}, {inter});')


