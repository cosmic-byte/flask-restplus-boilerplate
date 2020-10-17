import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from demjson import decode
from sklearn.metrics import r2_score
import sys
import os
import shutil


class gm11():

    def gmfit(self, x0, show):  # 自定义灰色预测函数
        x1 = x0.cumsum()  # 1-AGO序列
        x1 = pd.DataFrame(x1)
        z1 = (x1 + x1.shift()) / 2.0  # 紧邻均值（MEAN）生成序列
        z1 = z1[1:].values.reshape((len(z1) - 1, 1))  # 转成矩阵
        B = np.append(-z1, np.ones_like(z1), axis=1)  # 列合并-z1和形状同z1的1值矩阵  19X2
        Yn = x0[1:].reshape((len(x0) - 1, 1))  # 转成矩阵 19
        [[a], [b]] = np.dot(np.dot(np.linalg.inv(np.dot(B.T, B)), B.T), Yn)  # 计算参数，基于矩阵运算，np.dot矩阵相乘，np.linalg.inv矩阵求逆
        f = lambda k: (x0[0] - b / a) * np.exp(-a * (k - 1)) - (x0[0] - b / a) * np.exp(-a * (k - 2))  # 还原值
        delta = np.abs(x0 - np.array([f(i) for i in range(1, len(x0) + 1)]))  # 残差绝对值序列
        C = delta.std() / x0.std()
        P = 1.0 * (np.abs(delta - delta.mean()) < 0.6745 * x0.std()).sum() / len(x0)
        if show == 1:
            print('灰色模型的系数a:', a)
            print('灰色模型的系数b:', b)
            print('灰色模型的首项x0:', x0[0])
            print('小于0.35为优的方差比:', C)
            print('大于0.95为优的小残差概率:', P)
        return f, a, b, x0[0], C, P  # 返回灰色预测函数、a、b、首项、方差比、小残差概率

    def __init__(self, dataFileName, configFileName, outputPaths):
        self.write_path = outputPaths
        self.dataFileName = dataFileName
        self.configFileName = configFileName
        self.config = decode(open(self.configFileName).read())
        self.y_name = self.config['columnConfigs']['y']
        self.hyperParams = self.config['hyperParams']

    def start(self):
        self.org_stdout = sys.stdout
        try:
            shutil.rmtree(self.write_path)
        except:
            pass
        os.mkdir(self.write_path)
        self.f = open(self.write_path + '\\' + 'result.log', 'a')
        sys.stdout = self.f
        sys.stderr = self.f
        print('模型配置:', self.config)

    # 读取数据集的函数
    def readData(self):
        self.data = pd.read_csv(self.dataFileName)

    def run(self):
        self.y = self.data[self.y_name].values.reshape(-1)
        # 预测期数
        self.fr = self.hyperParams['forcast_tesq']
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        selx = ~np.isnan(self.y)[0:-1]

        df1 = np.diff(self.y)
        df1[np.isnan(df1)] = 0
        for i in range(self.fr):
            if i == 0:
                f = gm11.gmfit(self, df1, 1)[0]
            else:
                f = gm11.gmfit(self, df1, 0)[0]
            df1 = np.hstack((df1, f(len(df1))))
        dfx = df1[0:-self.fr]
        df1 = df1[-self.fr:]
        df3 = self.y[0:-1]
        df4 = dfx + df3

        print('真实值跟预测值的R^2:', r2_score(df3[selx], df4[selx]))

        for i in df1:
            self.y = np.hstack((self.y, self.y[-1] + i))
        # pd.DataFrame(df2, columns=['for']).to_csv('doge.csv', index=False)
        plt.plot(df3[selx], 'ro', label='真实值')
        plt.plot(self.y[np.hstack((selx, np.ones((self.fr + 1, 1)).reshape(-1).astype(bool)))], label='预测值')
        plt.title('预测值与真实值')
        plt.legend()
        plt.savefig(self.write_path + '\\' + 'forcast.png')
        # plt.show()
        self.forcast = self.y
        self.fit_values = df4[selx]

    # 输出结果使用的函数
    def output(self):
        sys.stdout = self.org_stdout
        self.f.close()
        # 写日志到路径
        # 保存图到路径
        # 压缩
        pass
