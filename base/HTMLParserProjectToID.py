#!/usr/bin/env python
#coding: utf-8
import re
import time
from HTMLParser import HTMLParser
from WriteEmailInfo import ConstructEmail
from bs4 import BeautifulSoup

class HTMLParserProjectToID(HTMLParser):
	"""docstring for ClassName"""
	project_tag="";
	project_value='';
	bfirstparseroption="";
	project_dict={};

	def handle_starttag(self,tag,attrs):
		#self.project_tag=tag;
		if tag == "option" and self.bfirstparseroption != False:
			for k, v in attrs:
				self.project_value=v;
			self.project_tag=tag;
			if self.bfirstparseroption=="":
				self.bfirstparseroption=True;
		else:
			if self.bfirstparseroption == True:
				self.bfirstparseroption=False;

	def handle_endtag(self,tag):
		self.project_tag="";
		self.projcet_attrs=[];
		self.project_value='';

	def handle_data(self,data):
		if self.project_tag == "option":
			self.project_dict[data]=self.project_value;

	def GetProjectId(self,project_name):
		if project_name in self.project_dict:
			return self.project_dict[project_name];
		else:
			print "can not get project id!!!";

class HTMLParserAssignedToByPerson(object):
	"""docstring for HTMLParserProjectByPerson"""
	def __init__(self, string):
		self.soup = BeautifulSoup(string,'lxml',from_encoding='utf-8');
		self.person_id_dict={};

	def ConstructPersonToIdList(self):
		for tag in self.soup.find_all('option'):
			if tag.has_attr('value'):
				username=tag.get_text();
				#print "username is: ",username;
				persionid=tag.attrs['value'];
				#print "persion id: ",persionid;
				self.person_id_dict[username]=persionid;

	def GetPersonId(self,username):
		if username in self.person_id_dict:
			#print "username is: ",username;
			#print "user project id:",self.person_id_dict[username];
			return self.person_id_dict[username];
		else:
			print "无法获取username 对应的user id"
			return "00000";

class HTMLPaserHideStatus(object):
	"""docstring for ClassName"""
	def __init__(self, string):
		self.soup = BeautifulSoup(string,'lxml',from_encoding='utf-8');
		self.hideStatus={};

	def ConstructHideStatus(self):
		for tag in self.soup.find_all('option'):
			if tag.has_attr('value'):
				hideStatu=tag.get_text();
				hideStatu_id=tag.attrs['value'];
				#print "hide Statu: ", hideStatu;
				#print "hide_Statu_id: ", hideStatu_id;
				self.hideStatus[hideStatu]=hideStatu_id;
				
	def GetHideStatusId(self,hideStatu_name):
		if hideStatu_name in self.hideStatus:
			#print "name: ",hideStatu_name;
			#print "hide Statu id: ", self.hideStatus[hideStatu_name];
			return self.hideStatus[hideStatu_name];
		else:
			#print "无法获取hide Status对应的id";
			print "00000";

class ParserHTMLOverDueMaintInfomations(object):

	"""docstring for ClassName"""
	def InitHTMLToBeautifulSoup(self, string):
		self.soup = BeautifulSoup(string,'lxml',from_encoding='utf-8');
		self.ID=0;
		self.Owner=0;
		self.DueDate=0;
		self.LastUpdate=0;
		self.summary=0;
		for tag in self.soup.find_all('tr',class_="row-category"):
			index=0;
			for child in tag.children:
				if child.name == 'td':
					if child.get_text()=="ID":
						self.ID=index;
					elif child.get_text()=="Status":
						self.Owner=index;
					elif child.get_text()=="Due Date":
						self.DueDate=index;
					elif child.get_text()== "Updated":
						self.LastUpdate=index;
					elif child.get_text()== "Summary":
						self.summary=index;
					index=index+1;

	def __defalutValue__(self):
		self.mantisId='';
		self.mantisOwner='';
		self.mantisDueDay='';
		self.mantisLastUpdate='';
		self.mantisDescription=''
		self.bIsStore=False;
		self.bIsOverDue=False;

	def open(self,filename):
		self.ConstructEmailHandle=ConstructEmail();
		self.ConstructEmailHandle.open(filename);
		self.emaillist=[];
		self.currenttime=time.strftime('%y-%m-%d',time.localtime(time.time()));
		#print self.currenttime;

	def ConstructEmail(self):
		#print self.soup.prettify();
		#print "html head contents name:",len(self.soup.head.contents);
		pattern_for_mantisowner=re.compile('\(.*\)');
		for tag in self.soup.find_all('tr'):
			if tag.has_attr('bgcolor') and tag.has_attr('border'):
				self.__defalutValue__();
				index=0;
				for child in tag.children:
					if child.name == 'td':
						if index == self.ID:#mantis id
							#print "mantis id: ",child.string;
							self.mantisId=child.string;
						elif index == self.Owner: #mantis owner
							for status in child.find_all('a'):
								if status.has_attr('title') and status.get('title') == "open":
									#print "this mantis need store";
									self.bIsStore=True;
							result=re.search(pattern_for_mantisowner,child.get_text());
							if result is None:
								print "mantis 未分配！！！";
								self.mantisOwner=None;
							else:
								#print "mantis owner:",result.group()[1:-1];
								#for string in child.strings:	
								self.mantisOwner=result.group()[1:-1];
						elif index == self.DueDate:#mantis due day
							#print "mantis DueDay:",child.string;
							self.mantisDueDay=child.string;
							if self.mantisDueDay is not None:	
								print self.mantisDueDay.split('-');
								if cmp(self.mantisDueDay,self.currenttime) < 0:
									self.bIsOverDue = True;
							else:
								print "due day 未填写！！！"
								self.mantisDueDay=None;
								self.bIsOverDue=True;
						elif index == self.LastUpdate:
							#print "mantis LastUpdate",child.string;
							self.mantisLastUpdate=child.string;
						elif index == self.summary:
							#print "mantis Description",child.string;
							self.mantisDescription=child.string;
						index=index+1;
				if self.bIsStore == True and self.bIsOverDue == True:
					print "这些mantis即将被需要存储："
					print "Mantis ID: ",self.mantisId;
					print "Mantis Description :",self.mantisDescription;
					print "Mantis Owner: ",self.mantisOwner;
					print "Manits DueDay: ",self.mantisDueDay;
					print "Mantis LastUpdate: ",self.mantisLastUpdate;
					print "\n";
					self.emaillist.append(self.mantisOwner);
					self.ConstructEmailHandle.WirteInfoMation(self.mantisId,self.mantisDescription,self.mantisDueDay,self.mantisLastUpdate,self.mantisOwner);

	def GetNextHTMLPage(self):
		url=None;
		for tag in self.soup.find_all('a'):
			if tag.has_attr('href') and tag.get_text() == "Next":
				if url == "http://mantis.mstarsemi.com/"+tag.get('href'):
					print "The same URL";
				else:
					print "has Next Page";
					url="http://mantis.mstarsemi.com/"+tag.get('href');
					print "url is: ",url;
		return url;

	def GetProjectEmailList(self):
		self.emaillist=list(set(self.emaillist));
		#debug 时打开
		#for index in xrange(len(self.emaillist)):
		#	print "即将发送邮件给这些人：",self.emaillist[index];
		return self.emaillist;

	def close(self):
		self.ConstructEmailHandle.close();
		del self.emaillist[:];