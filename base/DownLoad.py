#!/usr/bin/env python
#coding: utf-8
import urllib
import httplib

#download html form url
class DownLoadWeb(object):
	"""docstring for DownLoadWeb"""
	def __init__(self,handler):
		self.xmlhandler=handler;

	def StartDownLoad(self):
		login_url=self.xmlhandler.login_url;
		print login_url;
		#login the mantis web server!!!
		self.__Login__(login_url);


	def __DownLoad_Source_Get__(self,url):
		htmSource = ""
		try:
			urlx = httplib.urlsplit(url)
			conn = httplib.HTTPConnection(urlx.netloc)
			conn.connect()    #建立连接
			conn.putrequest("GET", url, None);    #请求类型
			conn.putheader("Content-Length", 0);
			conn.putheader("Connection", "keep-alive");
			conn.endheaders();

			res = conn.getresponse();
			htmSource = res.read();
		except Exception(), err:
			trackback.print_exec();
		finally:
			conn.close();  
		print htmSource;

	def __DownLoad_Source_Post__():
		print "need realize";

	def __Login__(self,url):
		print "need realize";