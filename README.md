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
	https://www.2cto.com/kf/201704/626050.html(特别注意文件夹的权限)
	如果遇到Python.h 找不到的错误，使用https://stackoverflow.com/questions/15631135/python-h-missing-from-ubuntu-12-04 进行解决