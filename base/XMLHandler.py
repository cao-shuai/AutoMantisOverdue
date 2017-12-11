#!/usr/bin/env python
#coding: utf-8
import os
import xml.sax
#xml handler for parser xml
class XMLHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.mail_host="";
        self.mailto_list=[];
        self.mailto_list_cc=[];
        self.mail_user="";
        self.mail_pass="";
        self.CurrentData="";
        self.mail_content_path="";
        self.mail_title="";

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
        elif self.CurrentData == "person":
            self.mailto_list.append(content);
        elif self.CurrentData == "person_cc":
        	self.mailto_list_cc.append(content);
