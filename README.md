# rec_service
基于flask的推荐系统接口服务
a recommendation service system based on flask

## 环境
```shell
# 新建python3.7环境
conda create -n recsvcpy37 python==3.7


# 安装依赖
pip install -r requirements.txt

# 导出项目依赖
pip install pipreqs
pipreqs ./ --encoding=utf8  --force # force参数覆盖当前路径下的requirements.txt
# 如果遇到报错ImportError: urllib3 v2.0 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with OpenSSL 1.1.0h  27 Mar 2018. 
# 更改urllib3版本：
pip install urllib3==1.26.15
```

## 目录说明