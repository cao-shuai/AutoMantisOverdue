#!/usr/bin/env python
#coding: utf-8
from base.SendEmail import Email
import xml.sax
from base.XMLHandler import XMLHandler
from base.DownLoad import DownLoadWeb
import sys

class TestClass(object):

	def TestXMLHandler(self):
		#create XML Reader
		parser=xml.sax.make_parser();
		#turn off namepsaces
		parser.setFeature(xml.sax.handler.feature_namespaces,0);
		#rewrite ContextHanler
		self.Handler=XMLHandler();
		parser.setContentHandler(self.Handler);
		parser.parse("./config/config.xml");

	def TestProjectS(self):
		self.TestXMLHandler();
		email=Email(self.Handler);
		html=DownLoadWeb(self.Handler);
		html.StartDownLoad();
		ProjectEmailList=html.GetProjectEmailList();
		for index in xrange(len(ProjectEmailList)):
			#print ProjectEmailList[index];
			for projectname in (ProjectEmailList[index]):
				print "需要发送邮件项目名称1: ",projectname;
				for x in xrange(len(ProjectEmailList[index][projectname])):
					print "需要发送邮件人的姓名1：",ProjectEmailList[index][projectname][x];
					email.AddEmailPerson(ProjectEmailList[index][projectname][x],"@mstarsemi.com");
				email.SendEmails("./out/"+projectname+".html");
		html.CloseDownLoad();

if __name__ == '__main__':
	reload(sys);
	sys.setdefaultencoding('utf-8');
	test=TestClass();
	test.TestProjectS();