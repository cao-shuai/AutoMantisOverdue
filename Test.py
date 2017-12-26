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
				print "项目名称: ",projectname;
				bIsNeedSendEmail=False;
				if len(ProjectEmailList[index][projectname]) == 0:
					print "太棒了，今天没有mantis overdue！！！"
				else:
					bIsNeedSendEmail=True;
					for x in xrange(len(ProjectEmailList[index][projectname])):
						if ProjectEmailList[index][projectname][x] is not None:
							print "需要发送邮件人的姓名：",ProjectEmailList[index][projectname][x];
							email.AddEmailPerson(ProjectEmailList[index][projectname][x],"@mstarsemi.com");
				#email.AddEmailPerson("scott.cao","@mstarsemi.com",True); #this will cc some person
				email.SendEmails("./out/"+projectname+".html",projectname,bIsNeedSendEmail);
		html.CloseDownLoad();

if __name__ == '__main__':
	reload(sys);
	sys.setdefaultencoding('utf-8');
	test=TestClass();
	test.TestProjectS();