#!/usr/bin/env python
#coding: utf-8
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import xml.sax


#xml handler for parser xml
class EmailHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.mail_host="";
        self.mailto_list=[];
        self.mail_user="";
        self.mail_pass="";
        self.CurrentData="";

    def startElement(self,tag,attributes):
        self.CurrentData=tag;

    def endElement(self,tag):
        self.CurrentData="";

    def characters(self,content):
        if self.CurrentData == "mail_host":
            self.mail_host=content;
        elif self.CurrentData == "mail_user":
            self.mail_user=content;
        elif self.CurrentData == "mail_password":
            self.mail_pass=content;
        elif self.CurrentData == "mail_title":
        	self.mail_title=content;
        elif self.CurrentData == "content-path":
        	self.mail_content_path=content;
        elif self.CurrentData == "perstion":
            self.mailto_list.append(content);

class Email(object):

    def __init__(self):
        #create XML Reader
        parser=xml.sax.make_parser();
        #turn off namepsaces
        parser.setFeature(xml.sax.handler.feature_namespaces,0);
        #rewrite ContextHanler
        Handler=EmailHandler();
        parser.setContentHandler(Handler);
        parser.parse("./config/config.xml");

        self.mail_host=Handler.mail_host;
        self.mail_user=Handler.mail_user;
        self.mail_pass=Handler.mail_pass;
        self.mailto_list=Handler.mailto_list;
        self.mail_title=Handler.mail_title;
        self.mail_content_path=Handler.mail_content_path;

    
    def SendEmails(self):
    	#construct email content!!!
    	#test info begin
    	try:
    		htmlf=open(self.mail_content_path);
	    	html = htmlf.read();
    	finally:
    		htmlf.close();
        #send email 
        if self.__send_mail__(html):
            return True;
        else:
            return False;

    def __send_mail__(self,html):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.mail_title;  
        msg['From'] = self.mail_user;
        msg['To'] = ";".join(self.mailto_list);
        part = MIMEText(html, 'html');
        msg.attach(part);

        try:
            server = smtplib.SMTP();
            server.connect(self.mail_host,25);
            server.login(self.mail_user,self.mail_pass);
            server.sendmail(self.mail_user, self.mailto_list, msg.as_string());
            server.close();
            return True;
        except (Exception):
            return False;
    	