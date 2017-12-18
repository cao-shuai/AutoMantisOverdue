#!/usr/bin/env python
#coding: utf-8
import urllib
import httplib
import urllib2
import cookielib
from HTMLParserProjectToID import HTMLParserProjectToID


#download html form url
class DownLoadWeb(object):
	"""docstring for DownLoadWeb"""
	def __init__(self,handler):
		self.xmlhandler=handler;
		self.htmlhandler='';
		self.parserhtmlhandler=''
		self.filter={};
		#this post data is username and password , need wiresharke get network packages
		self.data=urllib.urlencode({"username": self.xmlhandler.login_username,
			"password": self.xmlhandler.login_password});
		self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'};

	def StartDownLoad(self):
		login_url=self.xmlhandler.login_url;
		#login the mantis web server!!!
		self.__Login__(login_url);
		self.DownLoadProject(login_url);

	def __Login__(self,url):
		mycookie=cookielib.MozillaCookieJar();
		self.htmlhandler=urllib2.build_opener(urllib2.HTTPCookieProcessor(mycookie));
		result=self.htmlhandler.open(url,self.data);


	def DownLoadProject(self,starturl):
		self.__ConstructProjectIDList__(starturl);
		for item in self.xmlhandler.mantis_project_list:
			project_Id=self.parserhtmlhandler.GetProjectId(item);
			self.__DonwnLoadFromProjectId__(project_Id,item);

	def __DonwnLoadFromProjectId__(self,value,storehtmlfilename):
		#http post funtion url to set_project.php? and set project_id=value, can change the project id
		self.filter["project_id"]=value;
		self.htmlhandler.open("http://mantis.mstarsemi.com/set_project.php?",urllib.urlencode(self.filter));
		self.__savehtmlfile__("http://mantis.mstarsemi.com/view_all_bug_page.php",storehtmlfilename);
		
	#构建project id list 列表
	def __ConstructProjectIDList__(self,url):
		html_page=self.htmlhandler.open(url);
		self.parserhtmlhandler=HTMLParserProjectToID();
		self.parserhtmlhandler.feed(html_page.read());
		
	def __savehtmlfile__(self,url,filename):
		result=self.htmlhandler.open(url);
		with open("out/"+filename+".html","w") as f:
			f.write(result.read());