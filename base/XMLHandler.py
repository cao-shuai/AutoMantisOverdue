#!/usr/bin/env python
#coding: utf-8
import os
import copy
from bs4 import BeautifulSoup
#xml handler for parser xml
class XMLConfigHandler(object):
    """docstring for XMLHandler"""
    def __init__(self, string):
        self.main_url="";
        self.mail_host="";
        self.mail_user="";
        self.mail_pass="";
        self.mail_title="";
        self.login_url="";
        self.login_username="";
        self.login_password="";
        self.mantis_project_list={};
        self.emailserverinfo={};
        self.maintis_urlInfo={};
        #print string;
        self.soup=BeautifulSoup(string,'lxml',from_encoding='utf-8');

    def ParseXMLConfig(self):
        print "debug setp1";
        self.__ConstructEmailServerInfo__();
        self.__ConstructMaintServerInfo__();
        self.__ConstructMaintProjectsInfo__();
    
    def GetProjectList(self):
        projectsList=self.mantis_project_list.keys();
        print projectsList;
        return projectsList;    

    def GetProjectMaintsFilters(self,projectname,typename):
        #print "projectname is :",projectname;
        mantis_filters=self.mantis_project_list[projectname].get("mantis-filter");
        if typename in mantis_filters:
            print "prject filter type name: ",mantis_filters[typename];
            return mantis_filters[typename];
        else:
            print "can not get mantis fliter: ",typename;
            return 0;

    def GetProjectEmailCCTo(self,projectname):
        #print "projectname is :",projectname;
        email_list=self.mantis_project_list[projectname]["email-cc"];
        print email_list;
        return email_list;

    def GetSetOwnerListByProject(self,projectname):
        owner_list=self.mantis_project_list[projectname]["owner"];
        print owner_list;
        return owner_list;

    def GetEmailServerInfo(self,key):
        #for debug
        #for key in self.emailserverinfo:
        #    print "emailserverinfo key is :",key;
        #    print "emailserverinfo value is :",self.emailserverinfo[key];
        return self.emailserverinfo[key];

    def GetMaintsServerInfo(self,key):
        #for key in self.maintis_urlInfo:
        #    print "mantis serverinfo key is :",key;
        #    print "mantis serverinfo value is :",self.maintis_urlInfo[key];
        return self.maintis_urlInfo[key];

    def __ConstructEmailServerInfo__(self):
        for tag in self.soup.find_all("send_email_info"):
            for child in tag.children:
                if child.name is not None:
                    self.emailserverinfo[child.name]=child.get_text();

    def __ConstructMaintServerInfo__(self):
        for tag in self.soup.find_all("mantis_url"):
            for child in tag.children:
                if child.name is not None:
                    self.maintis_urlInfo[child.name]=child.get_text();

    def __ConstructMaintProjectsInfo__(self):
        for tag in self.soup.find_all('mantis_project'):
            #获取到一个mantis的信息
            currentProjectName="";
            mantisfilter={};
            emailccto=[];
            ownerList=[];
            for child in tag.children:
                if child.name == "mantis-project-name":
                    currentProjectName=child.get_text();
                elif child.name == "manits-filter":
                    if child.get("name") == "owner":
                        ownerList.append(child.get_text());
                    else:
                        mantisfilter[child.get("name")]=child.get_text();
                elif child.name == "email-cc":
                    emailccto.append(child.get_text());

            self.mantis_project_list[currentProjectName]={"mantis-filter": copy.deepcopy(mantisfilter),"email-cc":copy.deepcopy(emailccto),"owner": copy.deepcopy(ownerList)};
            #for debug
            for key in self.mantis_project_list:
                print "mantis_project_list key is: ",key;
                print "value", self.mantis_project_list[key];
                for key2 in self.mantis_project_list[key]:
                    print "debug!", self.mantis_project_list[key][key2];