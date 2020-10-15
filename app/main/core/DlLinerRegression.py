import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import numpy as np


class DlLinerRegression:

    def __init__(self, dataFileName, configFileName, outputFileName, **hyperPrams):
        self.dataFileName = dataFileName
        self.configFileName = configFileName
        self.outputFileName = outputFileName
        self.hyperPrams = hyperPrams

    # 读取数据集的函数
    def readData(self):
        self.data = pd.read_csv(self.dataFileName)

    # 主要的分析逻辑
    def run(self):
        X = self.data[['AT', 'V', 'AP', 'RH']]
        y = self.data[['PE']]

        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
        linreg = LinearRegression()
        linreg.fit(X_train, y_train)
        y_pred = linreg.predict(X_test)

        # 赋值留给output阶段使用
        self.linreg = linreg
        self.y_pred = y_pred
        self.y_test = y_test

    # 输出结果使用的函数
    def output(self):
        with open(self.outputFileName, "w+") as rsfile:
            rsfile.write("b = ")
            np.savetxt(rsfile, self.linreg.intercept_)
            rsfile.write("\n")
            rsfile.write("W = ")
            np.savetxt(rsfile, self.linreg.coef_)
            rsfile.write("\n")
            rsfile.write("predicate : \n")
            np.savetxt(rsfile, self.y_pred)
            rsfile.write("\n")
            print(metrics.mean_squared_error(self.y_test, self.y_pred))
            rsfile.write("MSE: {0}".format(metrics.mean_squared_error(self.y_test, self.y_pred)))
            rsfile.write("\n")
            rsfile.write("RMSE: {0}".format(np.sqrt(metrics.mean_squared_error(self.y_test, self.y_pred))))







