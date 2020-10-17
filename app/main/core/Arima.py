from statsmodels.tsa.stattools import adfuller
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_pacf, plot_acf
import statsmodels.tsa.stattools as st
import statsmodels.tsa.arima_model  as arima
from demjson import decode
import sys
import os
import shutil

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


class TSAArima:

    def autoARIMA(self):
        order = st.arma_order_select_ic(self.y, max_ar=3, max_ma=3, ic=['bic'])
        self.order_min = order.bic_min_order
        print('BIC信息准则选择的最优阶数')
        print(self.order_min)

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

    # 主要的分析逻辑
    def run(self):

        # self.x = self.data[self.X_name].values
        self.y = self.data[self.y_name].values.reshape(-1)

        print('ADF检验的结果')
        print(adfuller(self.y, autolag='AIC'))
        while adfuller(self.y, autolag='AIC')[1] > 0.1:
            print('ADF检验不通过,数据存在单位根,需要差分处理')
            self.y = np.diff(self.y)
            self.y = self.y[~np.isnan(self.y)]
        print('ADF检验的结果')
        dftest = adfuller(self.y, autolag='AIC')
        dfoutput = pd.Series(dftest[0:4], index=['检验统计量', 'p值', '滞后阶数', '用到的样本量'])
        # dftest的输出前一项依次为检测值，p值，滞后数，使用的观测数，各个置信度下的临界值
        for key, value in dftest[4].items():
            dfoutput['临界值(%s)' % key] = value
        print(dfoutput)

        fig = plot_acf(self.y)
        plt.title('自相关图')
        fig.savefig(self.write_path + '\\' + 'ACF.png')

        fig = plot_pacf(self.y)
        plt.title('偏自相关图')
        fig.savefig(self.write_path + '\\' + 'PACF.png')

        autoBIC = 1
        if autoBIC == 1:
            TSAArima.autoARIMA(self)
        else:
            self.order_min = [1, 1]
        model = arima.ARIMA(self.y, order=(self.order_min[0], 0, self.order_min[1]))
        result_ARIMA = model.fit(disp=-1)
        self.result = result_ARIMA.summary()
        self.resid = result_ARIMA.resid
        print(self.result)

    # 输出结果使用的函数
    def output(self):
        sys.stdout = self.org_stdout
        self.f.close()
        # 写日志到路径
        # 保存图到路径
        # 压缩
        pass
