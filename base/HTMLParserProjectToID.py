#!/usr/bin/env python
#coding: utf-8
from HTMLParser import HTMLParser

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