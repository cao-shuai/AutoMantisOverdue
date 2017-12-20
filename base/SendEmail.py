#!/usr/bin/env python
#coding: utf-8
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import copy

class Email(object):

    def __init__(self,Handler):
        self.mail_host=Handler.mail_host;
        self.mail_user=Handler.mail_user;
        self.mail_pass=Handler.mail_pass;
        self.mail_title=Handler.mail_title;
        self.parseby=Handler.parseby;
        if self.parseby == "Projects":
            self.mailto_list=[]
            self.mailto_list_cc=[];
            self.mail_recver=[];
        else:
            self.mailto_list=Handler.mailto_list;
            self.mailto_list_cc=Handler.mailto_list_cc;
            self.mail_recver=Handler.mail_recver;

    def AddEmailPerson(self,person,emailsuffix,bIsCC=False):
        personemail=person+emailsuffix;
        self.mail_recver.append(personemail);
        if bIsCC == False:
            self.mailto_list.append(personemail);
        else:
            self.mailto_list_cc.append(personemail);    

    def SendEmails(self,path):
    	try:
    		htmlf=open(path);
	    	html = htmlf.read();
    	finally:
    		htmlf.close();
        #send email 
        if self.__send_mail__(html):
            return True;
        else:
            return False;

    def __send_mail__(self,html):
        msg = MIMEMultipart('alternative');
        msg['Subject'] = self.mail_title;  
        msg['From'] = self.mail_user;
        msg['To'] = ",".join(self.mailto_list);
        msg['Cc'] = ",".join(self.mailto_list_cc);
        part=MIMEText(html,'html',_charset='UTF-8');
        msg.attach(part);

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