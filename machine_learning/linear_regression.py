from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import random
import copy

#获得data和label
def load_data():
    data = []
    deas = []
    data1 = []
    with open('../data/processed.cleveland.data', 'r') as f:
        m = f.readlines()
        for i in range(len(m)-3):
            arr = m[i].split(',')
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
for i in range(100):
    rand = random.randint(0, 299)
    train_data.append(m[rand])
    label_data.append(n[rand])


#测试精度
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
        #print(result)
    return tr/(tr+fa)

#画图
def mat(x_axis, y_axis):
    for i in range(len(x_axis)-1):
        plt.plot(x_axis, y_axis, color='r')
    plt.show()
    return 0

#进行训练linear
def lassoRegession(x, y, test, lab):
    data = []
    label = []
    x_axis = []
    y_axis = []
    linreg = LinearRegression()
    linreg.fit(x, y)
    for i in range(0,len(x),5):
        for j in x[i:i+5]:
            data.append(j)
        for t in y[i:i+5]:
            label.append(t)
        linreg.fit(data, label)
        x_axis.append(i + 5)
        y_axis.append(accurancy(test, lab, linreg))
    w = mat(x_axis, y_axis)
    return linreg


linreg = lassoRegession(train_data,label_data,m,n)
acc = accurancy(m,n,linreg)
print('[Linear Regression] The accuracy is: ', acc)
print(linreg.coef_)
