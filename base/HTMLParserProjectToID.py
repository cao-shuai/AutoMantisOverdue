#!/usr/bin/env python
#coding: utf-8
from HTMLParser import HTMLParser
from WriteEmailInfo import ConstructEmail

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
		return self.project_dict[project_name];

class HTMLParserOverDueMaintInfomation(HTMLParser):

	parserdata=[];
	bInManitsTable=False;
	bFirstData=False;#这个只是为了修复第一次给过来的data为不可见数据，还需要进一步分析，次为临时path
	bStore=False;
	emaillist=[];

	def open(self,filename):
		self.ConstructEmailHandle=ConstructEmail();
		self.ConstructEmailHandle.open(filename);

	def handle_starttag(self,tag,attrs):
		if tag == "tr":
			bInMantis=[False,False];
			for key,value in attrs:
				if key == "bgcolor":
					bInMantis[0]=True;
				elif key == "border":
					bInMantis[1]=True;
			if bInMantis[0] == True and bInMantis[1] == True:
				self.bInManitsTable=True;
				self.bFirstData=True;
				print "进入mantis Table 分析表!!!"
		elif self.bInManitsTable == True and tag == "a":
			 for key,value in attrs:
			 	  if key == "title": 
			 	  	if value == "open":
			 	  		self.bStore=True;
			 	  	else:
			 	  		self.bStore=False;

	def handle_endtag(self,tag):
		#print "End tag:",tag;
		if tag == "tr" and self.bInManitsTable == True:
			self.bInManitsTable=False;
			#for index in range(len(self.parserdata)):
			#	print "index:",index, "	vaule:",self.parserdata[index];
			if self.bStore == True:
				print "这些mantis即将被需要存储："
				print "Mantis ID: ",self.parserdata[0];
				print "Mantis Description :",self.parserdata[-1];
				print "Mantis Owner: ",self.parserdata[-5][2:-1];
				print "Manits DueDay: ",self.parserdata[-3];
				print "Mantis LastUpdate: ",self.parserdata[-2];
				self.emaillist.append(self.parserdata[-5][2:-1]);
				self.ConstructEmailHandle.WirteInfoMation(self.parserdata[0],self.parserdata[-1],self.parserdata[-3],self.parserdata[-2],self.parserdata[-5][2:-1]);
			del self.parserdata[:];
			print "离开mantis Table 分析表!!!"
			print "\n";

	def handle_data(self,data):
		if self.bInManitsTable == True:
			if self.bFirstData == False:
				self.parserdata.append(data);
			else:
				self.bFirstData=False;

	def GetProjectEmailList(self):
		self.emaillist=list(set(self.emaillist));
		#debug 时打开
		#for index in xrange(len(self.emaillist)):
		#	print "即将发送邮件给这些人：",self.emaillist[index];
		return self.emaillist;

	def close(self):
		self.ConstructEmailHandle.close();
		del self.parserdata[:];		
		del self.emaillist[:];