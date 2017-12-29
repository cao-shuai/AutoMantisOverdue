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

#download html form url
class DownLoadWeb(object):
	"""docstring for DownLoadWeb"""
	def __init__(self,handler):
		self.tempdirs="out/temp";
		self.xmlhandler=handler;
		self.htmlhandler='';
		self.parserhtmlhandler=''
		self.filter={};
		self.currentperson_idList=[];
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
		self.filter.clear();

	def __DownLoadProject__(self,starturl):
		self.__ConstructProjectIDList__(starturl);
		ProjectList=self.xmlhandler.GetProjectList();
		for index in xrange(len(ProjectList)):
			print "DownLoad Project name is: ",ProjectList[index];
			projectname=ProjectList[index];
			project_Id=self.parserhtmlhandler.GetProjectId(projectname);
			self.__DownLoadProjectByPerson__(project_Id,projectname);

	#构建project id list 列表
	def __ConstructProjectIDList__(self,url):
		html_page=self.htmlhandler.open(url);
		self.parserhtmlhandler=HTMLParserProjectToID();
		self.parserhtmlhandler.feed(html_page.read());
		html_page.close();
		self.parserhtmlhandler.close();

	def __DownLoadProjectByPerson__(self,value,projectname):
		#http post funtion url to set_project.php? and set project_id=value, can change the project id
		self.filter.clear();
		self.filter["project_id"]=value;
		self.htmlhandler.open(self.main_url+"/set_project.php?",urllib.urlencode(self.filter));
		#请求构造选择人对应的handle id
		result=self.htmlhandler.open(self.main_url+"/return_dynamic_filters.php?view_type=advanced&filter_target=handler_id_filter");
		html=HTMLParserAssignedToByPerson(result.read());
		result.close();
		html.ConstructPersonToIdList();
		personList=self.xmlhandler.GetSetOwnerListByProject(projectname);
		del self.currentperson_idList[:];
		self.currentperson_idList=copy.deepcopy(html.GetPersonIdList(personList));
		#请求构造选择hide status
		result=self.htmlhandler.open(self.main_url+'/return_dynamic_filters.php?view_type=advanced&filter_target=show_status_filter');
		html=HTMLPaserHideStatus(result.read());
		result.close();
		html.ConstructHideStatus();
		hideStatus=self.xmlhandler.GetProjectMaintsFilters(projectname,"hideStatus");
		self.currentHideStatus_id=html.GetHideStatusId(hideStatus);
		#发送对应人和hide status请求
		self.filter.clear();
		self.filter["type"]=self.xmlhandler.GetProjectMaintsFilters(projectname,"type");
		self.filter["view_type"]=self.xmlhandler.GetProjectMaintsFilters(projectname,"view_type");
		self.filter["page_number"]=self.xmlhandler.GetProjectMaintsFilters(projectname,"page_number");
		self.filter["per_page"]=self.xmlhandler.GetProjectMaintsFilters(projectname,"per_page");
		self.filter["handler_id"]=self.currentperson_idList[0];#需要修改
		self.filter["hide_status"]=self.currentHideStatus_id;
		self.filter["filter"]=self.xmlhandler.GetProjectMaintsFilters(projectname,"filter");
		result=self.htmlhandler.open(self.main_url+"/view_all_set.php?f=3",urllib.urlencode(self.filter));
		self.__SaveHtmlEmailFile__(self.main_url+"/view_all_bug_page.php",projectname);
		self.htmlhandler.close();

	def __Login__(self,url):
		mycookie=cookielib.MozillaCookieJar();
		self.htmlhandler=urllib2.build_opener(urllib2.HTTPCookieProcessor(mycookie));
		result=self.htmlhandler.open(url,self.data);
		self.htmlhandler.close();
		
	def __SaveHtmlEmailFile__(self,starturl,projectname):
		nexturl=starturl;
		html=ParserHTMLOverDueMaintInfomations();
		html.open(projectname);
		while nexturl is not None:
			result=self.htmlhandler.open(nexturl);
			html.InitHTMLToBeautifulSoup(result.read());
			result.close();
			html.ConstructEmail();
			nexturl=html.GetNextHTMLPage();
		emaillist=html.GetProjectEmailList();
		project_email={projectname: copy.deepcopy(emaillist)}; #特别留意深浅copy
		self.ProjectEmailList.append({projectname: copy.deepcopy(html.GetProjectEmailList())});#特别留意深浅copy
		html.close();
		self.htmlhandler.close();