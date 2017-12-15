#!/usr/bin/env python
#coding: utf-8
import urllib
import httplib
import urllib2
import cookielib

#download html form url
class DownLoadWeb(object):
	"""docstring for DownLoadWeb"""
	def __init__(self,handler):
		self.xmlhandler=handler;
		self.openhtmlhandler='';

	def StartDownLoad(self):
		login_url=self.xmlhandler.login_url;
		print login_url;
		#login the mantis web server!!!
		self.__Login__(login_url);
		self.__savehtmlfile__("http://mantis.mstarsemi.com/view_all_bug_page.php"); #for test

	def CloseDownLoad(self):
		self.openhtmlhandler.close();

	def __DownLoad_Source_Get__(self,url):
		print "need relize";

	def __DownLoad_Source_Post__():
		print "need realize";

	def __Login__(self,url):
		#this post data is username and password , need wiresharke get network packages
		postdata=urllib.urlencode({
			"username":self.xmlhandler.login_username,
			"password":self.xmlhandler.login_password
			});
		#save cookie to a file
		cookiefilename="out/mycookie.txt";
		mycookie=cookielib.MozillaCookieJar(cookiefilename);
		self.openhtmlhandler=urllib2.build_opener(urllib2.HTTPCookieProcessor(mycookie));
		self.openhtmlhandler.addheaders=[('User-Agent:','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36')];
		result=self.openhtmlhandler.open(url,postdata);
		mycookie.save(ignore_discard=True, ignore_expires=True);

	def __savehtmlfile__(self,url):
		result=self.openhtmlhandler.open(url);
		with open("out/ceshi.html","w") as f:
			f.write(result.read());