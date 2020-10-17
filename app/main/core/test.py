from Arima import TSAArima
from GM11 import gm11
import os
import zipfile

def zip_ya(start_dir):
    start_dir = start_dir  # 要压缩的文件夹路径
    file_news = start_dir + '.zip'  # 压缩后文件夹的名字

    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)
    for dir_path, dir_names, file_names in os.walk(start_dir):
        f_path = dir_path.replace(start_dir, '')  # 这一句很重要，不replace的话，就从根目录开始复制
        f_path = f_path and f_path + os.sep or ''  # 实现当前文件夹以及包含的所有文件的压缩
        for filename in file_names:
            z.write(os.path.join(dir_path, filename), f_path + filename)
    z.close()
    return file_news


outPaths="D:/PycharmProjects/flask-restplus-boilerplate/app/main/core/doge"
lr = gm11(dataFileName="data.csv",
              configFileName="config.cfg",
              outputPaths=outPaths)
lr.start()
lr.readData()
lr.run()
lr.output()
name=zip_ya(outPaths)
print(name)
