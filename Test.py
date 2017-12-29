#!/usr/bin/env python
#coding: utf-8
from base.SendEmail import Email
import os
from base.XMLHandler import XMLConfigHandler
from base.DownLoad import DownLoadWeb
import sys

class TestClass(object):
	def TestXMLHandler(self):
		with open("./config/config.xml") as filehandle:
			filehandle=open("./config/config.xml");
			self.Handler=XMLConfigHandler(filehandle.read());
			filehandle.close();
			self.Handler.ParseXMLConfig();
			projectlist=self.Handler.GetProjectList();
			#for index in xrange(len(projectlist)):
			#	print "project name: is: ",projectlist[index];
			#	print "mantis filter list is: ";
			#	self.Handler.GetProjectMaintsFilters(projectlist[index]);
			#	print "emaill cc list is: ";
			#	self.Handler.GetProjectEmailCCTo(projectlist[index]);

	def TestProjectS(self):
		self.TestXMLHandler();
		html=DownLoadWeb(self.Handler);
		html.StartDownLoad();
		ProjectEmailList=html.GetProjectEmailList();
		for index in xrange(len(ProjectEmailList)):
			#print ProjectEmailList[index];
			for projectname in (ProjectEmailList[index]):
				print "项目名称: ",projectname;
				email=Email(self.Handler);
				bIsNeedSendEmail=False;
				if len(ProjectEmailList[index][projectname]) == 0:
					print "太棒了，今天没有mantis overdue！！！"
				else:
					bIsNeedSendEmail=True;
					for x in xrange(len(ProjectEmailList[index][projectname])):
						if ProjectEmailList[index][projectname][x] is not None:
							print "需要发送邮件人的姓名：",ProjectEmailList[index][projectname][x];
							email.AddEmailPerson(ProjectEmailList[index][projectname][x],"@mstarsemi.com");
				email.SendEmails("./out/"+projectname+".html",projectname,bIsNeedSendEmail);
		html.CloseDownLoad();

if __name__ == '__main__':
	reload(sys);
	sys.setdefaultencoding('utf-8');
	test=TestClass();
	#test.TestXMLHandler();
	test.TestProjectS();