#!/usr/bin/env python
#coding: utf-8
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from XMLHandler import XMLConfigHandler
import copy

class Email(object):

    def __init__(self,Handler):
        self.xmlHanler=Handler;
        self.mail_host=Handler.GetEmailServerInfo("mail_host");
        print "mail host: ",self.mail_host;
        self.mail_user=Handler.GetEmailServerInfo("mail_user");
        print "mail user: ",self.mail_user;
        self.mail_pass=Handler.GetEmailServerInfo("mail_password");
        print "mail pass: ",self.mail_pass
        self.mail_title=Handler.GetEmailServerInfo("mail_title");
        print "mail title: ",self.mail_title;
        self.mailto_list=[];
        self.mailto_list_cc=[];
        self.mail_recver=[];


    def AddEmailPerson(self,person,emailsuffix="@mstarsemi.com",bIsCC=False):
        if bIsCC == False:
            personemail=person+emailsuffix;
            self.mailto_list.append(personemail);
        else:
            personemail=person;
            self.mailto_list_cc.append(personemail);
        self.mail_recver.append(personemail);

    def SendEmails(self,path,ProjectName,bhasOverDue=True):
        emailcctoList=self.xmlHanler.GetProjectEmailCCTo(ProjectName);
        for key in  xrange(len(emailcctoList)):
            print "email will be cc to: ",emailcctoList[key];
            self.AddEmailPerson(emailcctoList[key],bIsCC=True);
        if bhasOverDue == True:
            try:
                htmlf=open(path);
                self.html = htmlf.read();
            finally:
                htmlf.close();
        else:
            self.html="太棒了，今天没有mantis overdue！！！";

        #send email 
        if self.__send_mail__(ProjectName):
            return True;
        else:
            return False;

    def __send_mail__(self,ProjectName):
        msg = MIMEMultipart('alternative');
        msg['Subject'] = ProjectName+" "+self.mail_title;  
        msg['From'] = self.mail_user;
        msg['To'] = ",".join(self.mailto_list);
        msg['Cc'] = ",".join(self.mailto_list_cc);
        part=MIMEText(self.html,'html',_charset='UTF-8');
        msg.attach(part);
        #for index in xrange(len(self.mail_recver)):
        #    print "email is: ",self.mail_recver[index];
        #print "msg string",msg.as_string();
        try:
	        smtp = smtplib.SMTP();
	        smtp.connect(self.mail_host,25);
	        smtp.login(self.mail_user,self.mail_pass);
	        smtp.sendmail(self.mail_user, self.mail_recver, msg.as_string());
	        result=True;
        except Exception(), err:
            trackback.print_exec();
            result=False;
        finally:
            smtp.close();
        return result;