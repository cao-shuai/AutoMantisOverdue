#!/usr/bin/env python
#coding: utf-8
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import xml.sax
from email.header import Header
from base.XMLHandler import XMLHandler

class Email(object):

    def __init__(self):
        #create XML Reader
        parser=xml.sax.make_parser();
        #turn off namepsaces
        parser.setFeature(xml.sax.handler.feature_namespaces,0);
        #rewrite ContextHanler
        Handler=XMLHandler();
        parser.setContentHandler(Handler);
        parser.parse("./config/config.xml");

        self.mail_host=Handler.mail_host;
        self.mail_user=Handler.mail_user;
        self.mail_pass=Handler.mail_pass;
        self.mailto_list=Handler.mailto_list;
        self.mailto_list_cc=Handler.mailto_list_cc;
        self.mail_title=Handler.mail_title;
        self.mail_content_path=Handler.mail_content_path;
        self.mail_recver=Handler.mail_recver;

    
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
        msg = MIMEMultipart('alternative');
        msg['Subject'] = self.mail_title;  
        msg['From'] = self.mail_user;
        msg['To'] = ";".join(self.mailto_list);
        msg['Cc'] = ";".join(self.mailto_list_cc);
        part=MIMEText(html, 'html');
        msg.attach(part);

        try:
	        smtp = smtplib.SMTP();
	        smtp.connect(self.mail_host,25);
	        smtp.login(self.mail_user,self.mail_pass);
	        smtp.sendmail(self.mail_user, self.mail_recver, msg.as_string());
	        smtp.close();
	        return True;
        except (Exception):
        	return False;