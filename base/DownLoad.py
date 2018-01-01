#!/usr/bin/env python
#coding: utf-8
import os
import shutil
import urllib
import httplib
import urllib2
import cookielib
from HTMLParserProjectToID import HTMLParserProjectToID
from HTMLParserProjectToID import ParserHTMLOverDueMaintInfomations
from HTMLParserProjectToID import HTMLParserAssignedToByPerson
from HTMLParserProjectToID import HTMLPaserHideStatus
from XMLHandler import XMLConfigHandler
import copy
import threading

#download html form url
class DownLoadWeb(object):
	"""docstring for DownLoadWeb"""
	def __init__(self,handler):
		self.tempdirs="out/temp";
		self.xmlhandler=handler;
		self.htmlhandler='';
		self.parserhtmlhandler=''
		self.main_url=self.xmlhandler.GetMaintsServerInfo("main-url");
		#this post data is username and password , need wiresharke get network packages
		self.data=urllib.urlencode({"username": self.xmlhandler.GetMaintsServerInfo("login-username"),
			"password": self.xmlhandler.GetMaintsServerInfo("login-password")});
		self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'};
		self.ProjectEmailList=[];

	def StartDownLoad(self):
		login_url=self.xmlhandler.GetMaintsServerInfo("login-url");
		#login the mantis web server!!!
		self.__Login__(login_url);
		self.__DownLoadProject__(login_url);

	def GetProjectEmailList(self):
		return self.ProjectEmailList;

	def CloseDownLoad(self):
		del self.ProjectEmailList[:];

	def __DownLoadProject__(self,starturl):
		self.__ConstructProjectIDList__(starturl);
		ProjectList=self.xmlhandler.GetProjectList();
		thread=[];
		self.mylock=threading.RLock();
		for index in xrange(len(ProjectList)):
			print "DownLoad Project name is: ",ProjectList[index];
			projectname=ProjectList[index];
			project_Id=self.parserhtmlhandler.GetProjectId(projectname);
			#self.__DownLoadProjectByPerson__(project_Id,projectname);
			thread.append(threading.Thread(target=self.__DownLoadProjectByPerson__,args=(project_Id,projectname)));
			thread[index].start();
		for waitindex in xrange(len(thread)):
			thread[waitindex].join();

	#构建project id list 列表
	def __ConstructProjectIDList__(self,url):
		html_page=self.htmlhandler.open(url);
		self.parserhtmlhandler=HTMLParserProjectToID();
		self.parserhtmlhandler.feed(html_page.read());
		html_page.close();
		self.parserhtmlhandler.close();

	def __DownLoadProjectByPerson__(self,value,projectname):
		#http post funtion url to set_project.php? and set project_id=value, can change the project id
		filterdict={};
		filterdict["project_id"]=value;
		self.htmlhandler.open(self.main_url+"/set_project.php?",urllib.urlencode(filterdict));
		#请求构造选择人对应的handle id
		result=self.htmlhandler.open(self.main_url+"/return_dynamic_filters.php?view_type=advanced&filter_target=handler_id_filter");
		html=HTMLParserAssignedToByPerson(result.read());
		result.close();
		html.ConstructPersonToIdList();
		personList=self.xmlhandler.GetSetOwnerListByProject(projectname);
		currentperson_idList=[];
		currentperson_idList=copy.deepcopy(html.GetPersonIdList(personList));
		#请求构造选择hide status
		result=self.htmlhandler.open(self.main_url+'/return_dynamic_filters.php?view_type=advanced&filter_target=show_status_filter');
		html=HTMLPaserHideStatus(result.read());
		result.close();
		html.ConstructHideStatus();
		hideStatus=self.xmlhandler.GetProjectMaintsFilters(projectname,"hideStatus");
		currentHideStatus_id=html.GetHideStatusId(hideStatus);
		#发送对应人和hide status请求
		filterdict.clear();
		filterdict["type"]=self.xmlhandler.GetProjectMaintsFilters(projectname,"type");
		filterdict["view_type"]=self.xmlhandler.GetProjectMaintsFilters(projectname,"view_type");
		filterdict["page_number"]=self.xmlhandler.GetProjectMaintsFilters(projectname,"page_number");
		filterdict["per_page"]=self.xmlhandler.GetProjectMaintsFilters(projectname,"per_page");
		filterdict["hide_status"]=currentHideStatus_id;
		filterdict["filter"]=self.xmlhandler.GetProjectMaintsFilters(projectname,"filter");
		currentprojecthtmlhander=ParserHTMLOverDueMaintInfomations();
		for index in xrange(len(currentperson_idList)):
			filterdict["handler_id"]=currentperson_idList[index];#需要修改
			result=self.htmlhandler.open(self.main_url+"/view_all_set.php?f=3",urllib.urlencode(filterdict));
			self.__SaveHtmlEmailFile__(self.main_url+"/view_all_bug_page.php",projectname,currentprojecthtmlhander,index);
		emaillist=currentprojecthtmlhander.GetProjectEmailList();
		#project_email={projectname: copy.deepcopy(emaillist)}; #特别留意深浅copy
		self.mylock.acquire();
		self.ProjectEmailList.append({projectname: copy.deepcopy(currentprojecthtmlhander.GetProjectEmailList())});#特别留意深浅copy
		self.mylock.release();
		currentprojecthtmlhander.close();
		self.htmlhandler.close();

	def __Login__(self,url):
		mycookie=cookielib.MozillaCookieJar();
		self.htmlhandler=urllib2.build_opener(urllib2.HTTPCookieProcessor(mycookie));
		result=self.htmlhandler.open(url,self.data);
		self.htmlhandler.close();
		
	def __SaveHtmlEmailFile__(self,starturl,projectname,html,index):
		nexturl=starturl;
		if index == 0:
			html.open(projectname);
		while nexturl is not None:
			result=self.htmlhandler.open(nexturl);
			html.InitHTMLToBeautifulSoup(result.read());
			result.close();
			html.ConstructEmail();
			nexturl=html.GetNextHTMLPage();