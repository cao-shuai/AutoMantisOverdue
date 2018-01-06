# AutoMantisOverdue
1. 环境准备：
   自己的机器信息：eg: cat /proc/version
   inux version 3.16.0-30-generic (buildd@kissel) (gcc version 4.8.2 (Ubuntu 4.8.2-19ubuntu1) ) #40~14.04.1-Ubuntu SMP Thu Jan 15 17:43:14 UTC 2015
   python版本：2.7：
   环境配置方法参考网上配置
2. 需要依赖的第三方库：
   需要安装BeautifulSoup，
   安装方法：easy_install beautifulsoup4 或 pip intall beautifulsoup4 或apt-get install Python-bs4
3. python gevent 的配置方法可以参考如下链接：
	https://www.2cto.com/kf/201704/626050.html (特别注意文件夹的权限)
	其实很简单，记录在这里给有需要的朋友，大多数问题其实是出在easy_install 上的，遇到此类问题，最好能去下个源包，比如这个：
	https://pypi.python.org/packages/source/g/gevent/gevent-0.13.1.tar.gz#md5=5c1b03d9ce39fee4cfe5ea8befb1d4c4
	解压后，要先运行下其中的：
	1) python fetch_libevent.py
	2) python setup.py build
 	3) python setup.py install
	如果遇到Python.h 找不到的错误我的系统就无法找到：
	参考：使用https://stackoverflow.com/questions/15631135/python-h-missing-from-ubuntu-12-04 进行解决：
	如下命令： sudo apt-get  update; sudo apt-get install  python-dev -y