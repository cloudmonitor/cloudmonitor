# CloudMonitor
> 利用flask提供后台api接口

下载完成之后记得安装`requirements.txt`中提到的库
```bash
pip install -r requirements.txt
```

由于将`osapi`单独提取出来了，因此还需要安装`osapi`,具体参见[osapi](https://github.com/cloudmonitor/osapi)

测试运行
```bash
python manager.py runserver --host 192.168.1.100 --port 5000
```

也可以利用`uwsgi+nginx`部署flask引用参见[uwsgi+nginx部署flask应用](https://henulwj.github.io/2016/04/18/flask-uwsgi-nginx/)