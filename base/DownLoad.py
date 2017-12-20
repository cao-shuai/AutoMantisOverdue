#!/usr/bin/env python
#coding: utf-8
import os
import shutil
import urllib
import httplib
import urllib2
import cookielib
from HTMLParserProjectToID import HTMLParserProjectToID
from HTMLParserProjectToID import HTMLParserOverDueMaintInfomation
import copy

#download html form url
class DownLoadWeb(object):
	"""docstring for DownLoadWeb"""
	def __init__(self,handler):
		self.tempdirs="out/temp";
		self.xmlhandler=handler;
		self.htmlhandler='';
		self.parserhtmlhandler=''
		self.filter={};
		#this post data is username and password , need wiresharke get network packages
		self.data=urllib.urlencode({"username": self.xmlhandler.login_username,
			"password": self.xmlhandler.login_password});
		self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'};
		self.ProjectEmailList=[];

	def StartDownLoad(self):
		login_url=self.xmlhandler.login_url;
		#login the mantis web server!!!
		self.__Login__(login_url);
		self.__DownLoadProject__(login_url);

	def GetProjectEmailList(self):
		return self.ProjectEmailList;

	def CloseDownLoad(self):
		del self.ProjectEmailList[:];
		self.filter.clear();

	def __DownLoadProject__(self,starturl):
		self.__ConstructProjectIDList__(starturl);
		for projectname in self.xmlhandler.mantis_project_list:
			project_Id=self.parserhtmlhandler.GetProjectId(projectname);
			self.__DonwnLoadFromProjectId__(project_Id,projectname);

	#构建project id list 列表
	def __ConstructProjectIDList__(self,url):
		html_page=self.htmlhandler.open(url);
		self.parserhtmlhandler=HTMLParserProjectToID();
		self.parserhtmlhandler.feed(html_page.read());
		self.parserhtmlhandler.close();

	def __DonwnLoadFromProjectId__(self,value,projectname):
		#http post funtion url to set_project.php? and set project_id=value, can change the project id
		self.filter["project_id"]=value;
		self.htmlhandler.open(self.xmlhandler.main_url+"/set_project.php?",urllib.urlencode(self.filter));
		self.__SaveHtmlEmailFile__(self.xmlhandler.main_url+"/print_all_bug_page.php",projectname);
		self.htmlhandler.close();

	def __Login__(self,url):
		mycookie=cookielib.MozillaCookieJar();
		self.htmlhandler=urllib2.build_opener(urllib2.HTTPCookieProcessor(mycookie));
		result=self.htmlhandler.open(url,self.data);
		self.htmlhandler.close();
		
	def __SaveHtmlEmailFile__(self,url,projectname):
		result=self.htmlhandler.open(url);
		html=HTMLParserOverDueMaintInfomation();
		html.open(projectname);
		html.feed(result.read());
		#emaillist=html.GetProjectEmailList();
		#project_email={projectname: copy.deepcopy(emaillist)}; #特别留意深浅copy
		self.ProjectEmailList.append({projectname: copy.deepcopy(html.GetProjectEmailList())});#特别留意深浅copy
		html.close();
		self.htmlhandler.close();